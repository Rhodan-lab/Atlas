import assert from "node:assert/strict";
import test from "node:test";

import { routeApi } from "../src/api.ts";
import { AtlasRuntime, type CommandRunner } from "../src/runtime.ts";

function makeRuntime(calls: Array<{ executable: string; args: string[] }>): AtlasRuntime {
    const runner: CommandRunner = async (executable, args) => {
        calls.push({ executable, args });
        if (args[0] === "stats-json") {
            return { stdout: '{"concepts":7,"relations":9,"formatVersion":1}\n', stderr: "" };
        }
        if (executable === "search-bin") {
            return { stdout: '{"query":"graph","count":0,"results":[]}\n', stderr: "" };
        }
        return { stdout: '{"concepts":[]}\n', stderr: "" };
    };
    return new AtlasRuntime(
        { dataFile: "data.atlas", coreBinary: "core-bin", searchBinary: "search-bin" },
        runner,
    );
}

test("stats route delegates to the C++ JSON command", async () => {
    const calls: Array<{ executable: string; args: string[] }> = [];
    const response = await routeApi(new URL("http://localhost/api/stats"), makeRuntime(calls));
    assert.equal(response?.status, 200);
    assert.deepEqual(response?.body, { concepts: 7, relations: 9, formatVersion: 1 });
    assert.deepEqual(calls[0], {
        executable: "core-bin",
        args: ["stats-json", "data.atlas"],
    });
});

test("search route delegates to Rust and enforces a bounded limit", async () => {
    const calls: Array<{ executable: string; args: string[] }> = [];
    const response = await routeApi(
        new URL("http://localhost/api/search?q=graph&limit=5"),
        makeRuntime(calls),
    );
    assert.equal(response?.status, 200);
    assert.deepEqual(calls[0], {
        executable: "search-bin",
        args: ["data.atlas", "graph", "--limit", "5"],
    });

    await assert.rejects(
        () => routeApi(new URL("http://localhost/api/search?q=x&limit=101"), makeRuntime([])),
        /between 1 and 100/,
    );
});

test("missing search query returns a client error without invoking a process", async () => {
    const calls: Array<{ executable: string; args: string[] }> = [];
    const response = await routeApi(new URL("http://localhost/api/search"), makeRuntime(calls));
    assert.deepEqual(response, {
        status: 400,
        body: { error: "query parameter q is required" },
    });
    assert.equal(calls.length, 0);
});
