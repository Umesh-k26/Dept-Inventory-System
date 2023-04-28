import React from "react";
import { getSession } from "next-auth/react";
import { AddOrder, UpdateOrder, DisplayOrders } from "components/User/Order";
import {
  AddAsset,
  UpdateAsset,
  DisplayAssets,
  AssetsBarcode,
} from "components/User/Asset";
import {
  AddBulkAsset,
  UpdateBulkAsset,
  DisplayBulkAssets,
  BulkAssetsBarcode
} from "components/User/BulkAsset";
import { useState } from "react";
import UserNav from "components/UserNav";

const User = () => {
  const [selectedOption, setSelectedOption] = useState(null);

  const handleOptionClick = (option, callback) => {
    setSelectedOption(option);
    // console.log(selectedOption);
    callback();
  };
  return (
    <>
      <UserNav
        handleOptionClick={handleOptionClick}
        selectedOption={selectedOption}
      />

      {selectedOption == 1 && <AddAsset />}
      {selectedOption == 2 && <UpdateAsset />}
      {selectedOption == 3 && <DisplayAssets />}
      {selectedOption == 4 && <AssetsBarcode />}
      {selectedOption == 11 && <AddBulkAsset />}
      {selectedOption == 22 && <UpdateBulkAsset />}
      {selectedOption == 33 && <DisplayBulkAssets />}
      {selectedOption == 44 && < BulkAssetsBarcode/>}
      {selectedOption == 111 && <AddOrder />}
      {selectedOption == 222 && <UpdateOrder />}
      {selectedOption == 333 && <DisplayOrders />}
    </>
  );
};

export default User;

export async function getServerSideProps(context) {
  const { req } = context;
  const session = await getSession({ req });

  if (!session?.ok) {
    return {
      redirect: {
        destination: "/",
        shallow: true,
      },
    };
  }
  return {
    props: {
      session,
    },
  };
}
