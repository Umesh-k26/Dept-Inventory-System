import React from "react";
import { AddUser, DeleteUser, UpdateUser } from "components/Admin/User";
import { AddAsset, DeleteAsset, UpdateAsset } from "components/User/Asset";
import { AddOrder, DeleteOrder, UpdateOrder } from "components/User/Order";
import AdminNav from "components/Admin/AdminNav";
import DataTable from "components/Table";
import { getSession } from "next-auth/react";
import { useState } from "react";

const Admin = ({ session }) => {
  if (!session) {
    return <p>Loading...</p>;
  }

  const [selectedOption, setSelectedOption] = useState(null);

  const handleOptionClick = (option, callback) => {
    setSelectedOption(option);
    console.log(selectedOption)
    callback();
    // setIsOpen(false);
  };
  // create a responsive subnavbar containing user, asset, order, related drop down menus
  return (
    <>
      <AdminNav
        handleOptionClick={handleOptionClick}
        selectedOption={selectedOption}
      />

      {selectedOption === 1 && <AddUser />}
      {selectedOption === 2 && <UpdateUser />}
      {selectedOption === 3 && <DeleteUser />}
      {selectedOption === 11 && <AddAsset />}
      {selectedOption === 22 && <UpdateAsset />}
      {selectedOption === 33 && <DeleteAsset />}
      {selectedOption === 111 && <AddOrder />}
      {selectedOption === 222 && <UpdateOrder />}
      {selectedOption === 333 && <DeleteOrder />}
    </>
  );
};

export default Admin;

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
