import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

export type CommandRunner = (
    executable: string,
    args: string[],
) => Promise<{ stdout: string; stderr: string }>;

export interface RuntimeConfig {
    dataFile: string;
    coreBinary: string;
    searchBinary: string;
}

async function defaultRunner(executable: string, args: string[]): Promise<{ stdout: string; stderr: string }> {
    const result = await execFileAsync(executable, args, {
        encoding: "utf8",
        maxBuffer: 4 * 1024 * 1024,
        timeout: 15_000,
    });
    return { stdout: result.stdout, stderr: result.stderr };
}

function parseJsonOutput(output: string, command: string): JsonValue {
    try {
        return JSON.parse(output) as JsonValue;
    } catch (error) {
        throw new Error(`${command} returned invalid JSON: ${(error as Error).message}`);
    }
}

export class AtlasRuntime {
    readonly config: RuntimeConfig;
    readonly runner: CommandRunner;

    constructor(config: RuntimeConfig, runner: CommandRunner = defaultRunner) {
        this.config = config;
        this.runner = runner;
    }

    private async core(command: string, ...args: string[]): Promise<JsonValue> {
        const result = await this.runner(this.config.coreBinary, [command, this.config.dataFile, ...args]);
        return parseJsonOutput(result.stdout, `atlas ${command}`);
    }

    async stats(): Promise<JsonValue> {
        return this.core("stats-json");
    }

    async concepts(): Promise<JsonValue> {
        return this.core("list-json");
    }

    async neighbors(id: number): Promise<JsonValue> {
        return this.core("neighbors-json", String(id));
    }

    async path(from: number, to: number): Promise<JsonValue> {
        return this.core("path-json", String(from), String(to));
    }

    async search(query: string, limit: number): Promise<JsonValue> {
        const result = await this.runner(this.config.searchBinary, [
            this.config.dataFile,
            query,
            "--limit",
            String(limit),
        ]);
        return parseJsonOutput(result.stdout, "atlas-search");
    }
}
