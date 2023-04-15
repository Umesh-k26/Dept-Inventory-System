import React from "react";
import { AddAsset, DeleteAsset, UpdateAsset } from "components/User/Asset";
import { AddOrder, DeleteOrder, UpdateOrder } from "components/User/Order";
import MUIDataTable from "mui-datatables";

const User = () => {
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

  const options = {
    filterType: "dropdown",
    download: true,
    print: true,
    selectableRows: "multiple",
    responsive: "vertical",
  };

  return (
    <>
      {/* <MUIDataTable data={data} columns={columns} options={options} /> */}
      <h1>User</h1>

      <div>Add Asset</div>
      <AddAsset />
      <hr />
      <div>Delete Asset</div>
      <DeleteAsset />
      <hr />
      <div>Update Asset</div>
      <UpdateAsset />
      <hr />
      <div>Add order</div>
      <AddOrder />
      <hr />
      <div>Delete Order</div>
      <DeleteOrder />
      <hr />
      <div>Update Order</div>
      <UpdateOrder />
    </>
  );
};

export default User;
