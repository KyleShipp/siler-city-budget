/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production';

const nextConfig = {
  output: 'export',
  basePath: isProd ? '/chatham-nc-budget' : '',
  images: { unoptimized: true },
};

module.exports = nextConfig;
