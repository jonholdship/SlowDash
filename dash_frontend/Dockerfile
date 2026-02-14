FROM node:22-alpine AS builder

WORKDIR /app

# Build argument for backend API base URL (used at build time by Next.js)
ARG NEXT_PUBLIC_API_BASE_URL=http://backend:8000/
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# Install deps
COPY package.json package-lock.json* pnpm-lock.yaml* ./
RUN npm install --legacy-peer-deps

# Copy source and build
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Copy production node_modules
COPY package.json ./
RUN npm install --production --legacy-peer-deps

# Copy built assets
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.mjs ./next.config.mjs

EXPOSE 3000
CMD ["npx", "next", "start", "-p", "3000"]
