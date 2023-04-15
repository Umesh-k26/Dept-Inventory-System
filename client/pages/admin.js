import React from "react";
import { AddUser, DeleteUser, UpdateUser } from "components/Admin/User";
import DataTable from "components/Table";

// import
const Admin = () => {
  return (
    <>
      {/* <DataTable
        apiLink={"http://localhost:8000/get-all-user"}
        method={"GET"}
        tableName={"Users List"}
      /> */}
      <DataTable />
      <AddUser />
      <DeleteUser />
      <UpdateUser />
    </>
  );
};

export default Admin;
