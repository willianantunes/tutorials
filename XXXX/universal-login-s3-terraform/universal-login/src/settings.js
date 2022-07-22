const IS_PRODUCTION = process.env.NODE_ENV === "production"
const ASSET_PREFIX = process.env.ASSET_PREFIX

module.exports = {
  IS_PRODUCTION,
  ASSET_PREFIX,
}
