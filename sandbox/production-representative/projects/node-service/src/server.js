const http = require("http");

function createApp(config = {}) {
  const serviceName = config.serviceName || "node-service";
  const maxLatencyMs = Number(config.maxLatencyMs || 250);
  return {
    serviceName,
    maxLatencyMs,
    handle(pathname) {
      if (pathname === "/health") return { status: 200, body: { ok: true, serviceName } };
      if (pathname === "/ready") return { status: 200, body: { ready: true, maxLatencyMs } };
      return { status: 404, body: { error: "NOT_FOUND" } };
    }
  };
}

function start(port = 0, config = {}) {
  const app = createApp(config);
  const server = http.createServer((request, response) => {
    const result = app.handle(new URL(request.url, "http://localhost").pathname);
    response.writeHead(result.status, { "content-type": "application/json" });
    response.end(JSON.stringify(result.body));
  });
  return new Promise((resolve) => server.listen(port, () => resolve({ server, app })));
}

module.exports = { createApp, start };
