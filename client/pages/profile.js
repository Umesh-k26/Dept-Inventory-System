import React from "react";
import { signOut, useSession } from "next-auth/react";
import { AssetDetails } from "components/Admin/AssetDetails";

const Profile = () => {
  const { data: session, status } = useSession();
  return (
    <>
      <div>Welcome {session?.user.name}</div>
      <AssetDetails />
      <button onClick={() => signOut({ callbackUrl: "/" })}>Sign Out</button>
    </>
  );
};

export default Profile;
