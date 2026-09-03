import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import styles from "./index.module.css";

const features = [
  {
    title: "Incident Reporting",
    description:
      "Multi-step guided form with a 17-category harm taxonomy. Students document privacy violations with context-appropriate harm classification.",
  },
  {
    title: "Privacy by Design",
    description:
      "Concealment workflow allows students to request identity protection. Admins review and grant or deny. Redacted in all exports.",
  },
  {
    title: "27 Support Resources",
    description:
      "Curated library of real Nigerian organisations, NDPC, NPF-NCCC, MANI, Asido Foundation, and more, matched to incidents by type and harm.",
  },
  {
    title: "PDF Export",
    description:
      "Structured PDF reports with unique PRG-XXXXXXXX reference codes, per-incident identity redaction, and bulk export with table of contents.",
  },
  {
    title: "Security First",
    description:
      "Argon2 password hashing, 15-minute session timeout, CSRF protection, secure cookies, audit logging, and input sanitisation.",
  },
  {
    title: "Admin Dashboard",
    description:
      "7-filter search, concealment grant/deny workflow, harm distribution analytics, and severity breakdown, all in a responsive dark/light interface.",
  },
];

function Feature({ title, description }) {
  return (
    <div className={clsx("feature-card")}>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <img
          src="img/logo.svg"
          alt="PrivGuard Logo"
          className={styles.heroLogo}
        />
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro"
          >
            Read the Docs
          </Link>
          <Link
            className="button button--secondary button--outline button--lg"
            to="/docs/installation"
            style={{ marginLeft: "1rem" }}
          >
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title="Documentation"
      description={siteConfig.tagline}
    >
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {features.map((props, idx) => (
                <div key={idx} className={clsx("col col--4")}>
                  <Feature {...props} />
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
