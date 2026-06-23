function releaseSummary(projects) {
  const ready = projects.filter((project) => project.status === "ready").length;
  return { total: projects.length, ready, blocked: projects.length - ready };
}

module.exports = { releaseSummary };
