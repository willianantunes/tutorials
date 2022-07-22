const { ASSET_PREFIX, IS_PRODUCTION } = require("./src/settings")

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // https://nextjs.org/docs/api-reference/next.config.js/cdn-support-with-asset-prefix
  assetPrefix: IS_PRODUCTION ? ASSET_PREFIX : "",
}

module.exports = nextConfig
