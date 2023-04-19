import React from "react";
import { AddUser, DeleteUser, UpdateUser, DisplayUsers } from "components/Admin/User";
import { AddAsset, DeleteAsset, UpdateAsset, DisplayAssets } from "components/User/Asset";
import { AddOrder, DeleteOrder, UpdateOrder, DisplayOrders } from "components/User/Order";
import AdminNav from "components/Admin/AdminNav";
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
      {selectedOption === 4 && <DisplayUsers />}
      {selectedOption === 11 && <AddAsset />}
      {selectedOption === 22 && <UpdateAsset />}
      {selectedOption === 33 && <DeleteAsset />}
      {selectedOption === 44 && <DisplayAssets />}
      {selectedOption === 111 && <AddOrder />}
      {selectedOption === 222 && <UpdateOrder />}
      {selectedOption === 333 && <DeleteOrder />}
      {selectedOption === 444 && <DisplayOrders />}
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
