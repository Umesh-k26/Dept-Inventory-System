import React from "react";
import { getSession } from "next-auth/react";

const Profile = ({ session }) => {
  if (!session) return <p>Loading...</p>;
  return (
    <div>
      <div>Welcome {session?.user.name}</div>
    </div>
  );
};

export default Profile;

export async function getServerSideProps(context) {
  const { req } = context;
  const session = await getSession({ req });
  if (!session) {
    return {
      redirect: { destination: "/", shallow: true },
    };
  }
  return {
    props: {
      session,
    },
  };
}
