import React, { useState, useEffect } from "react";
import { signIn, getProviders, getSession, useSession } from "next-auth/react";
import AdminNav from "components/Navbars/AdminNav";
import UserNav from "components/Navbars/UserNav";

const Home = ({ providers, role }) => {
  const { data: session, status } = useSession();

  if (status === "authenticated") {
    return (
      <>
        <p>You are signed in as {session.user.email}</p>
        <p>Your role is {role}</p>
        {role == "Admin" && <AdminNav />}
        {role != "Admin" && <UserNav />}
      </>
    );
  }
  return (
    <>
      <h2>{session?.message}</h2>
      <div className="min-h-screen bg-gray-100 flex flex-col justify-center py-8 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <div className="space-y-6">
              {providers &&
                Object.values(providers).map((provider) => {
                  return (
                    <div key={provider.name}>
                      <button
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        onClick={() => signIn(provider.id)}
                      >
                        Sign in with {provider.name}
                      </button>
                    </div>
                  );
                })}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;

export async function getServerSideProps(context) {
  const providers = await getProviders();
  const { req } = context;
  const session = await getSession({ req });
  let role = null;
  if (session) {
    role = await getRole(session.accessToken);
  }
  // console.log("from index.js", session);

  return {
    props: {
      providers,
      role,
    },
  };
}

const getRole = async (token) => {
  try {
    const res = await fetch("http://localhost:8000/get-role/", {
      headers: {
        Authorization: token,
      },
    });
    const data = await res.json();
    return data.user_type;
  } catch (err) {
    console.log(err);
  }
};
