/**
 * Eleventy configuration for And Chillax
 *
 * Strategy:
 * - Eleventy ONLY processes markdown blog posts in /blog/_posts/
 * - All other files (HTML pages, CSS, images, admin, etc) are passed through unchanged
 * - Output goes to _site/ which Netlify publishes
 *
 * The existing static HTML pages (homepage, courses, about, contact, etc) keep
 * working exactly as before. Only the blog is "managed" by Eleventy + the CMS.
 */

const fs = require("fs");
const path = require("path");

module.exports = function (eleventyConfig) {

  // ----------------------------------------------------------------------
  // Pass-through static files (deploy as-is, no processing)
  // ----------------------------------------------------------------------
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("_redirects");
  eleventyConfig.addPassthroughCopy("sitemap.xml");
  eleventyConfig.addPassthroughCopy("robots.txt");
  eleventyConfig.addPassthroughCopy("404.html");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("site_main_logo1.png");
  eleventyConfig.addPassthroughCopy("humans.txt");
  eleventyConfig.addPassthroughCopy("data");

  // Top-level pages (existing static HTML, not Eleventy-managed)
  eleventyConfig.addPassthroughCopy("index.html");
  eleventyConfig.addPassthroughCopy("about.html");
  eleventyConfig.addPassthroughCopy("contact.html");
  eleventyConfig.addPassthroughCopy("baby-massage.html");
  eleventyConfig.addPassthroughCopy("doula-services.html");
  eleventyConfig.addPassthroughCopy("reviews.html");
  eleventyConfig.addPassthroughCopy("leave-a-review.html");
  eleventyConfig.addPassthroughCopy("thanks.html");

  // Sub-directory static pages
  // The existing 9 blog posts stay as static HTML (passthrough). The CMS
  // only manages NEW posts in /blog/_posts/*.md. Migration of old posts
  // can come later if Eva wants to edit them via the CMS.
  eleventyConfig.addPassthroughCopy("blog/*.html");
  eleventyConfig.addPassthroughCopy("courses/*.html");

  // ----------------------------------------------------------------------
  // Date filter — for nicely formatted dates in templates
  // ----------------------------------------------------------------------
  eleventyConfig.addFilter("date", (dateObj, format) => {
    const d = new Date(dateObj);
    if (format === "iso") return d.toISOString().split("T")[0];
    if (format === "human") {
      return d.toLocaleDateString("en-GB", {
        year: "numeric", month: "long", day: "numeric"
      });
    }
    return d.toString();
  });

  // ----------------------------------------------------------------------
  // Collections — let templates query "all blog posts ordered by date"
  // ----------------------------------------------------------------------
  eleventyConfig.addCollection("posts", (collection) => {
    return collection.getFilteredByGlob("blog/_posts/*.md")
      .sort((a, b) => b.data.date - a.data.date);
  });

  // ----------------------------------------------------------------------
  // Output config
  // ----------------------------------------------------------------------
  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    // Templates are processed in this order
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    // Source files Eleventy will process (ignore everything else)
    templateFormats: ["md", "njk"],
    // Pretty URLs — output blog/baby-choking/ instead of blog/baby-choking.html
    pathPrefix: "/"
  };
};
