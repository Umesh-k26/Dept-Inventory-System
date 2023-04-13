import React from "react";
import { AddUser, DeleteUser } from "components/Admin/User";
// import 
const Admin = () => {
  // const { data: session, status } = useSession();
  return (
    <>
      <div>Admin</div>
      <AddUser />
      <DeleteUser />
    </>
  );
};

export default Admin;
