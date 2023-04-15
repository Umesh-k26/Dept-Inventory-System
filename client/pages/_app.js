import { SessionProvider } from "next-auth/react";
import "styles/globals.css";
import Layout from "components/layouts";

export default function App({ Component, pageProps }) {
  return (
    <>
      <SessionProvider>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </SessionProvider>
    </>
  );
}
