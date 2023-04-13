import React from "react";
import { signIn, getProviders, getSession } from "next-auth/react";

const Home = ({ providers }) => {
  return (
    <>
      <p className="underline font-bold">hello world</p>
      {providers &&
        Object.values(providers).map((provider) => {
          return (
            <div key={provider.name} style={{ marginBottom: 0 }}>
              <button onClick={() => signIn(provider.id)}>
                Sign in with {provider.name}
              </button>
            </div>
          );
        })}
    </>
  );
};

export default Home;

export async function getServerSideProps(context) {
  const providers = await getProviders();
  const { req } = context;
  const session = await getSession({ req });
  if (session) {
    return {
      redirect: { destination: "/profile" },
    };
  }
  return {
    props: {
      providers,
    },
  };
}
