import React from "react";
import { AddUser, DeleteUser, UpdateUser } from "components/Admin/User";
import DataTable from "components/Table";

// import
const Admin = () => {
  const data = [
    ["John Doe", "johndoe@gmail.com", "Male", "25"],
    ["Jane Smith", "janesmith@gmail.com", "Female", "30"],
    ["Bob Johnson", "bobjohnson@gmail.com", "Male", "45"],
    ["Mary Davis", "marydavis@gmail.com", "Female", "32"],
  ];
  
  
  
  const columns = [
    {
      name: "Name",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "Email",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "Gender",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "Age",
      options: {
        filter: false,
        sort: true,
      },
    },
  ];
  // const { data: session, status } = useSession();
  return (
    <>
      <div>Admin</div>
      <AddUser />
      <DeleteUser />
      <UpdateUser />
      <DataTable
        apiLink={"http://localhost:8000/get-all-user"}
        method={"GET"}
      />
    </>
  );
};

export default Admin;
