import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer, type ServerResponse } from "node:http";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

import { routeApi } from "./api.ts";
import { AtlasRuntime } from "./runtime.ts";

const moduleDirectory = fileURLToPath(new URL(".", import.meta.url));
const publicDirectory = normalize(join(moduleDirectory, "../public"));
const port = Number(process.env.PORT ?? "4242");
const host = process.env.HOST ?? "127.0.0.1";

const runtime = new AtlasRuntime({
    dataFile: process.env.ATLAS_DATA ?? "data/starter.atlas",
    coreBinary: process.env.ATLAS_CORE_BIN ?? "build/engine/cpp/atlas",
    searchBinary: process.env.ATLAS_SEARCH_BIN ?? "services/search-rs/target/release/atlas-search",
});

const contentTypes: Record<string, string> = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
};

function sendJson(response: ServerResponse, status: number, body: unknown): void {
    response.writeHead(status, {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "no-store",
    });
    response.end(JSON.stringify(body));
}

async function serveStatic(pathname: string, response: ServerResponse): Promise<void> {
    const requested = pathname === "/" ? "/index.html" : pathname;
    const candidate = normalize(join(publicDirectory, requested));
    if (!candidate.startsWith(publicDirectory)) {
        sendJson(response, 403, { error: "forbidden" });
        return;
    }

    try {
        const metadata = await stat(candidate);
        if (!metadata.isFile()) {
            throw new Error("not a file");
        }
        response.writeHead(200, {
            "content-type": contentTypes[extname(candidate)] ?? "application/octet-stream",
            "content-length": metadata.size,
        });
        createReadStream(candidate).pipe(response);
    } catch {
        sendJson(response, 404, { error: "not found" });
    }
}

const server = createServer(async (request, response) => {
    try {
        const url = new URL(request.url ?? "/", `http://${request.headers.host ?? "localhost"}`);
        const apiResponse = await routeApi(url, runtime);
        if (apiResponse) {
            sendJson(response, apiResponse.status, apiResponse.body);
            return;
        }
        await serveStatic(url.pathname, response);
    } catch (error) {
        const message = error instanceof Error ? error.message : "unknown error";
        const status = error instanceof RangeError ? 400 : 502;
        sendJson(response, status, { error: message });
    }
});

server.listen(port, host, () => {
    console.log(`Atlas local API listening at http://${host}:${port}`);
    console.log(`Data: ${runtime.config.dataFile}`);
});
