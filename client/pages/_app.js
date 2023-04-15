import { SessionProvider } from "next-auth/react";
import "styles/globals.css";
import Layout from "components/layouts";
import Container from "components/Container";

export default function App({ Component, pageProps }) {
  return (
    <>
      <SessionProvider>
        <Layout>
          <Container>
            <Component {...pageProps} />
          </Container>
        </Layout>
      </SessionProvider>
    </>
  );
}
