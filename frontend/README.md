# Natal Chart Generation Frontend

This is the frontend for the Lens X Astrace Natal Chart Generation App. It has a simple landing page and a form page for birth information. The form page only becomes accessible when the user connects to Polygon with their Web3 wallet.

<table>
  <tr>
    <td>
      <img src="./assets/landing_page.png" alt="Landing page" height="300"/>
      <br>
      <em>Landing page</em>
    </td>
    <td>
      <img src="./assets/form_page.png" alt="Form page" height="300"/>
      <br>
      <em>Form page</em>
    </td>
  </tr>
</table>

## Overview

- This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).
- Web3 wallet integration is handled using [web3-react](https://www.npmjs.com/package/web3-react).
- There's a bit of complex logic behind what is displayed to the user depending on whether their wallet is connected and to which network. That logic is shown in [this](./assets/wallet%20connection%20flowchart.pdf) diagram.
- Form inputs are customized [MUI Autocomplete components](https://mui.com/material-ui/react-autocomplete/).
- The [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview) is used to autocomplete input for birth city.
- Deployment is done via Vercel. See Deployment section.

## Requirements
- Node.js 14.6.0 or newer

## Getting Started

In the `frontend` directory, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Figma Design Files

Figma design files can be found [here](https://www.figma.com/file/YIFQ1a77HUtXqQk87830pF/Astrace---Website?node-id=741-23909&t=KdAV4NrbABOnXg7k-0).

## Component Design and Structure

The structure of the React components and how they relate to one another *should* be straightforward.

**One important note**: The website is designed as a single page. That is, the landing "page" and the form "page" are not, in fact, separate pages. They are two separate *components* rendered on the same page depending on certain logic. See logic map [here](./assets/wallet%20connection%20flowchart.pdf).

## Deployment

- Set up a [Vercel](https://vercel.com/) account and project, and add `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID` as [secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
  - See instructions [here](https://vercel.com/guides/how-can-i-use-github-actions-with-vercel#configuring-github-actions-for-vercel) on how to get these values.
- Deployment should be entirely handled by [this](../.github/workflows/deploy-frontend-to-vercel.yml) Github Actions workflow. That is, anytime there is a push made to the `production` branch, the frontend will be deployed via [Vercel CLI](https://vercel.com/docs/cli). 
- Setting up a custom domain can be done via the Vercel website. See [here](https://vercel.com/docs/concepts/projects/domains/add-a-domain).

