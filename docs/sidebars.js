/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    {
      type: "doc",
      id: "intro",
      label: "Introduction",
    },
    {
      type: "category",
      label: "Getting Started",
      collapsed: false,
      items: [
        "installation",
        "configuration",
      ],
    },
    {
      type: "category",
      label: "Architecture",
      collapsed: false,
      items: [
        "architecture",
        "project-structure",
      ],
    },
    {
      type: "category",
      label: "Features",
      collapsed: false,
      items: [
        "features/incident-reporting",
        "features/harm-taxonomy",
        "features/concealment-workflow",
        "features/support-resources",
        "features/pdf-export",
        "features/security",
      ],
    },
    {
      type: "category",
      label: "Deployment",
      collapsed: false,
      items: [
        "deployment/vercel",
        "deployment/docker",
        "deployment/manual",
      ],
    },
    {
      type: "doc",
      id: "testing",
      label: "Testing",
    },
    {
      type: "doc",
      id: "contributing",
      label: "Contributing",
    },
  ],
};

export default sidebars;
