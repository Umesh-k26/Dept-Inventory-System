import React from "react";
import { AddAsset, DeleteAsset, UpdateAsset} from "components/User/Asset";
import { AddOrder, DeleteOrder, UpdateOrder } from "components/User/Order"
import DataTable from "components/Table";


const User = () => {
  return (
    <>
      <h1>User</h1>

      <div>Add Asset</div>
      <AddAsset/>
      <hr/>
      <div>Delete Asset</div>
      <DeleteAsset/>
      <hr/>
      <div>Update Asset</div>
      <UpdateAsset/>
      <hr/>
      <div>Add order</div>
      <AddOrder/>
      <hr/>
      <div>Delete Order</div>
      <DeleteOrder/>
      <hr/>
      <div>Update Order</div>
      <UpdateOrder/>
      <DataTable
        apiLink={"http://localhost:8000/get-all-user"}
        method={"GET"}
      />

    </>
  );
};

export default User;
