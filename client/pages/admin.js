import React from "react";
import { AddUser, DeleteUser, UpdateUser } from "components/Admin/User";
// import
const Admin = () => {
  // const { data: session, status } = useSession();
  return (
    <>
      <div>Admin</div>
      <AddUser />
      <DeleteUser />
      <UpdateUser />
    </>
  );
};

export default Admin;
