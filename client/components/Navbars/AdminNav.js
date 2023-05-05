import React from "react";
import {
  AddUser,
  ActivateDeactivateUser,
  UpdateUser,
  DisplayUsers,
} from "components/User";
import {
  AddAsset,
  DeleteAsset,
  UpdateAsset,
  DisplayAssets,
  AssetsBarcode,
} from "components/Asset";
import {
  AddBulkAsset,
  DeleteBulkAsset,
  UpdateBulkAsset,
  DisplayBulkAssets,
  BulkAssetsBarcode,
} from "components/BulkAsset";
import {
  AddOrder,
  DeleteOrder,
  UpdateOrder,
  DisplayOrders,
} from "components/Order";
import DisplayNav from "./DisplayNav";

const AdminNav = () => {
  const options = {
    User: [
      {
        id: 1,
        name: "Add User",
        prop: AddUser,
      },
      {
        id: 2,
        name: "Update User",
        prop: UpdateUser,
      },
      {
        id: 3,
        name: "Activate/ Deactivate User",
        prop: ActivateDeactivateUser,
      },
      {
        id: 4,
        name: "Display Users",
        prop: DisplayUsers,
      },
    ],
    Asset: [
      {
        id: 11,
        name: "Add Asset",
        prop: AddAsset,
      },
      {
        id: 22,
        name: "Update Asset",
        prop: UpdateAsset,
      },
      {
        id: 33,
        name: "Delete Asset",
        prop: DeleteAsset,
      },
      {
        id: 44,
        name: "Display Assets",
        prop: DisplayAssets,
      },
      {
        id: 55,
        name: "Assets Barcode",
        prop: AssetsBarcode,
      },
    ],
    "Bulk Asset": [
      {
        id: 111,
        name: "Add Bulk Asset",
        prop: AddBulkAsset,
      },
      {
        id: 222,
        name: "Update Bulk Asset",
        prop: UpdateBulkAsset,
      },
      {
        id: 333,
        name: "Delete Bulk Asset",
        prop: DeleteBulkAsset,
      },
      {
        id: 444,
        name: "Display Bulk Assets",
        prop: DisplayBulkAssets,
      },
      {
        id: 555,
        name: "Bulk Assets Barcode",
        prop: BulkAssetsBarcode,
      },
    ],
    Order: [
      {
        id: 1111,
        name: "Add Order",
        prop: AddOrder,
      },
      {
        id: 2222,
        name: "Update Order",
        prop: UpdateOrder,
      },
      {
        id: 3333,
        name: "Delete Order",
        prop: DeleteOrder,
      },
      {
        id: 4444,
        name: "Display Orders",
        prop: DisplayOrders,
      },
    ],
  };

  return <DisplayNav types={options} />;
};

export default AdminNav;
