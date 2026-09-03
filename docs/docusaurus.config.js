// @ts-check
import { themes as prismThemes } from "prism-react-renderer";

const config = {
  title: "PrivGuard",
  tagline: "Privacy Incident Reporting System for Nigerian University Students",
  favicon: "img/favicon.svg",

  url: "https://trinnode.github.io",
  baseUrl: "/PrivGuard/",

  organizationName: "trinnode",
  projectName: "PrivGuard",

  onBrokenLinks: "throw",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: "./sidebars.js",
          editUrl:
            "https://github.com/trinnode/PrivGuard/tree/main/docs/",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: "img/social-card.png",
      navbar: {
        title: "PrivGuard",
        logo: {
          alt: "PrivGuard Logo",
          src: "img/logo.svg",
        },
        items: [
          {
            type: "docSidebar",
            sidebarId: "docsSidebar",
            position: "left",
            label: "Documentation",
          },
          {
            href: "https://github.com/trinnode/PrivGuard",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Documentation",
            items: [
              { label: "Getting Started", to: "/docs/intro" },
              { label: "Installation", to: "/docs/installation" },
              { label: "Architecture", to: "/docs/architecture" },
            ],
          },
          {
            title: "Community",
            items: [
              {
                label: "GitHub Issues",
                href: "https://github.com/trinnode/PrivGuard/issues",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "PrivGuard",
                href: "https://github.com/trinnode/PrivGuard",
              },
            ],
          },
        ],
        copyright: `Built for academic research. Django ${new Date().getFullYear()} PrivGuard.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: [
          "bash",
          "python",
          "sql",
          "docker",
          "json",
          "yaml",
        ],
      },
    }),
};

export default config;
