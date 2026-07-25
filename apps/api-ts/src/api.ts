import type { AtlasRuntime, JsonValue } from "./runtime.ts";

export interface ApiResponse {
    status: number;
    body: JsonValue;
}

function positiveInteger(raw: string | null, name: string, maximum = Number.MAX_SAFE_INTEGER): number {
    if (raw === null || !/^\d+$/.test(raw)) {
        throw new RangeError(`${name} must be a positive integer`);
    }
    const value = Number(raw);
    if (!Number.isSafeInteger(value) || value <= 0 || value > maximum) {
        throw new RangeError(`${name} must be between 1 and ${maximum}`);
    }
    return value;
}

export async function routeApi(url: URL, runtime: AtlasRuntime): Promise<ApiResponse | null> {
    if (!url.pathname.startsWith("/api/")) {
        return null;
    }

    if (url.pathname === "/api/health") {
        return {
            status: 200,
            body: {
                status: "ok",
                service: "atlas-local-api",
                dataFile: runtime.config.dataFile,
            },
        };
    }

    if (url.pathname === "/api/stats") {
        return { status: 200, body: await runtime.stats() };
    }

    if (url.pathname === "/api/concepts") {
        return { status: 200, body: await runtime.concepts() };
    }

    if (url.pathname === "/api/search") {
        const query = (url.searchParams.get("q") ?? "").trim();
        if (!query) {
            return { status: 400, body: { error: "query parameter q is required" } };
        }
        const rawLimit = url.searchParams.get("limit");
        const limit = rawLimit === null ? 10 : positiveInteger(rawLimit, "limit", 100);
        return { status: 200, body: await runtime.search(query, limit) };
    }

    const neighborsMatch = url.pathname.match(/^\/api\/concepts\/(\d+)\/neighbors$/);
    if (neighborsMatch) {
        const id = positiveInteger(neighborsMatch[1], "concept id");
        return { status: 200, body: await runtime.neighbors(id) };
    }

    if (url.pathname === "/api/path") {
        const from = positiveInteger(url.searchParams.get("from"), "from");
        const to = positiveInteger(url.searchParams.get("to"), "to");
        return { status: 200, body: await runtime.path(from, to) };
    }

    return { status: 404, body: { error: "API route not found" } };
}
