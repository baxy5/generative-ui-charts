import React from "react";
import {
  Info,
  TrendingUp,
  TrendingDown,
  XCircle,
  Lightbulb,
} from "lucide-react";

const DesignSystem = () => {
  const renderColorPalette = () => (
    <div className="grid-container-auto-large">
      <div className="bg-dark padding-md">--bg-dark</div>
      <div className="bg-primary padding-md">--bg-primary</div>
      <div className="bg-secondary padding-md">--bg-secondary</div>
      <div className="bg-tertiary padding-md">--bg-tertiary</div>
      <div className="bg-card-light padding-md">--card-bg-light</div>
      <div className="bg-card-medium padding-md">--card-bg-medium</div>
      <div className="bg-card-dark padding-md">--card-bg-dark</div>
      <div className="padding-md text-light bg-dark">--text-light</div>
      <div className="padding-md text-accent bg-dark">--text-accent</div>
      <div className="padding-md text-highlight bg-dark">--text-highlight</div>
      <div className="padding-md accent-dark bg-light">--accent-dark</div>
      <div className="padding-md accent-primary bg-light">--accent-primary</div>
    </div>
  );

  const renderTypography = () => (
    <div>
      <p className="title-main">Main Title (.title-main)</p>
      <p className="title-section">Section Title (.title-section)</p>
      <p className="title-subsection">Subsection Title (.title-subsection)</p>
      <p className="title-card">Card Title (.title-card)</p>
      <p className="text-regular">
        Regular text (.text-regular) - The quick brown fox jumps over the lazy
        dog.
      </p>
      <p className="text-small">
        Small text (.text-small) - The quick brown fox jumps over the lazy dog.
      </p>
      <p className="text-caption">
        Caption text (.text-caption) - The quick brown fox jumps over the lazy
        dog.
      </p>
      <div
        className="flex-container-start"
        style={{ alignItems: "baseline", gap: "2rem" }}
      >
        <p className="metric-large">1.2M</p>
        <p className="metric-medium">850K</p>
        <p className="metric-small">95k</p>
      </div>
    </div>
  );

  const renderButtonsAndInputs = () => (
    <div className="flex-container-column" style={{ gap: "1rem" }}>
      <div className="flex-container-start">
        <button className="clear-filter-btn">Clear Filter</button>
        <button className="btn-clear">Clear</button>
        <button className="toggle-button">Toggle</button>
      </div>
      <div className="filter-container">
        <input
          type="text"
          className="filter-input"
          placeholder="Filter input..."
        />
        <input
          type="text"
          className="input-search"
          placeholder="Search input..."
        />
      </div>
    </div>
  );

  const renderStatusBadgesAndTags = () => (
    <div className="flex-container-column" style={{ gap: "1rem" }}>
      <div className="flex-container-start">
        <span className="status-badge-positive">Positive</span>
        <span className="status-badge-negative">Negative</span>
        <span className="status-badge-neutral">Neutral</span>
        <span className="status-badge-info">Info</span>
      </div>
      <div className="tag-container">
        <span className="tag">Default Tag</span>
        <span className="tag tag-variant-outlined">Outlined Tag</span>
        <span className="tag tag-primary">Primary Tag</span>
        <span className="tag tag-secondary">Secondary Tag</span>
      </div>
    </div>
  );

  const renderCards = () => (
    <div className="grid-container-3">
      {/* Standard Card */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Standard Card</h3>
          <p className="card-subtitle">Subtitle for card</p>
        </div>
        <div className="card-body">
          <p>This is the body of the standard card.</p>
        </div>
        <div className="card-footer">
          <p>Footer content</p>
        </div>
      </div>
      {/* Elevated Card */}
      <div className="card card-variant-elevated">
        <div className="card-header">
          <h3 className="card-title">Elevated Card</h3>
        </div>
        <div className="card-body">
          <p>This card has an elevated style with a shadow.</p>
        </div>
      </div>
      {/* Bordered Card */}
      <div className="card card-variant-bordered">
        <div className="card-header">
          <h3 className="card-title">Bordered Card</h3>
        </div>
        <div className="card-body">
          <p>This card has a distinct border.</p>
        </div>
      </div>
    </div>
  );

  const renderLayoutContainers = () => (
    <div>
      <h3 className="title-subsection">Flex Containers</h3>
      <div className="flex-container-between component-container padding-md">
        <div>Item 1</div>
        <div>Item 2</div>
        <div>Item 3</div>
      </div>
      <h3 className="title-subsection" style={{ marginTop: "1rem" }}>
        Grid Containers
      </h3>
      <div className="grid-container-3 component-container padding-md">
        <div className="bg-tertiary padding-sm">Grid Item 1</div>
        <div className="bg-tertiary padding-sm">Grid Item 2</div>
        <div className="bg-tertiary padding-sm">Grid Item 3</div>
        <div className="bg-tertiary padding-sm">Grid Item 4</div>
        <div className="bg-tertiary padding-sm">Grid Item 5</div>
        <div className="bg-tertiary padding-sm">Grid Item 6</div>
      </div>
    </div>
  );

  const renderComponentExamples = () => (
    <div className="grid-container-2">
      {/* Stat Box */}
      <div className="stat-box">
        <p className="stat-title">Total Revenue</p>
        <p className="stat-value">$4,024</p>
        <div className="stat-change-positive">
          <TrendingUp size={16} /> 12.5%
        </div>
        <p className="stat-description">vs. last month</p>
      </div>
      <div className="stat-box stat-box-variant-elevated">
        <p className="stat-title">Subscriptions</p>
        <p className="stat-value">2,350</p>
        <div className="stat-change-negative">
          <TrendingDown size={16} /> -2.1%
        </div>
        <p className="stat-description">vs. last month</p>
      </div>

      {/* Info Panel */}
      <div className="info-panel">
        <h4 className="info-title">Information Panel</h4>
        <p className="info-content">
          This is a standard info panel with some details.
        </p>
        <div className="info-footer">
          <Info size={14} />
          <span>Footer Note</span>
        </div>
      </div>
      <div className="info-panel info-panel-variant-alert">
        <h4 className="info-title">Alert!</h4>
        <p className="info-content">
          This is an alert info panel for important messages.
        </p>
        <div className="info-footer">
          <XCircle size={14} />
          <span>Critical</span>
        </div>
      </div>

      {/* KPI Box */}
      <div className="kpi-box">
        <p id="title">User Growth</p>
        <p id="metric">15.2%</p>
        <p id="difference-positive">+2.1%</p>
        <p id="description">Monthly growth rate</p>
      </div>

      {/* Hero Section */}
      <div className="hero-section">
        <h2 className="hero-title">Hero Title</h2>
        <p className="hero-subtitle">
          This is a compelling subtitle for the hero section.
        </p>
        <button className="hero-cta">Call to Action</button>
      </div>
    </div>
  );

  const renderDataTable = () => (
    <div className="data-table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th className="sortable interactive-header">
              Product <span className="sort-indicator">↑</span>
            </th>
            <th>Sales</th>
            <th className="sortable interactive-header">
              Status <span className="sort-indicator">↓</span>
            </th>
            <th>Trend</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Product A</td>
            <td>5,400</td>
            <td>
              <span className="status-badge-positive">Active</span>
            </td>
            <td className="value-positive">+5%</td>
          </tr>
          <tr>
            <td>Product B</td>
            <td>3,210</td>
            <td>
              <span className="status-badge-negative">Inactive</span>
            </td>
            <td className="value-negative">-2%</td>
          </tr>
          <tr>
            <td>Product C</td>
            <td>4,800</td>
            <td>
              <span className="status-badge-neutral">Pending</span>
            </td>
            <td className="value-neutral">0%</td>
          </tr>
        </tbody>
      </table>
    </div>
  );

  const renderPromptSuggestions = () => (
    <div className="prompt-suggestions-container">
      <h3 className="prompt-suggestions-title flex items-center gap-2">
        <Lightbulb size={24} /> Prompt Suggestions
      </h3>
      <div className="prompt-suggestions-grid">
        <div className="prompt-suggestion-item">
          <h4 className="item-title">
            &quot;Show me the sales trend for the last quarter&quot;
          </h4>
          <p className="item-subtitle">
            Generates a line chart for sales data.
          </p>
        </div>
        <div className="prompt-suggestion-item">
          <h4 className="item-title">
            &quot;List all available books in the fantasy genre&quot;
          </h4>
          <p className="item-subtitle">
            Creates a table of books filtered by genre.
          </p>
        </div>
        <div className="prompt-suggestion-item">
          <h4 className="item-title">
            &quot;What is the average rating of books by J.R.R. Tolkien?&quot;
          </h4>
          <p className="item-subtitle">
            Displays a KPI card with the calculated average rating.
          </p>
        </div>
        <div className="prompt-suggestion-item">
          <h4 className="item-title">
            &quot;Compare the number of copies for &apos;Dune&apos; and
            &apos;1984&apos;&quot;
          </h4>
          <p className="item-subtitle">
            Generates a bar chart comparing two items.
          </p>
        </div>
      </div>
    </div>
  );

  const Section = ({
    title,
    children,
  }: {
    title: string;
    children: React.ReactNode;
  }) => (
    <section className="component-container padding-lg mb-8">
      <h2
        className="title-section padding-bottom-md"
        style={{ borderBottom: "1px solid var(--bg-tertiary)" }}
      >
        {title}
      </h2>
      {children}
    </section>
  );

  return (
    <div className="min-h-screen bg-primary padding-2xl custom-scroll">
      <header className="text-center mb-12">
        <h1 className="title-main">GenUI Design System</h1>
        <p className="text-regular text-accent">
          A comprehensive guide to the UI components and styles.
        </p>
      </header>

      <main>
        <Section title="Color Palette">{renderColorPalette()}</Section>
        <Section title="Typography">{renderTypography()}</Section>
        <Section title="Buttons & Inputs">{renderButtonsAndInputs()}</Section>
        <Section title="Status Badges & Tags">
          {renderStatusBadgesAndTags()}
        </Section>
        <Section title="Cards">{renderCards()}</Section>
        <Section title="Component Examples">
          {renderComponentExamples()}
        </Section>
        <Section title="Data Table">{renderDataTable()}</Section>
        <Section title="Layout Containers">{renderLayoutContainers()}</Section>
        <Section title="Prompt Suggestions">
          {renderPromptSuggestions()}
        </Section>
      </main>
    </div>
  );
};

export default DesignSystem;
