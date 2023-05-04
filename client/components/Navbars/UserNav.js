import React from "react";
import { AddOrder, UpdateOrder, DisplayOrders } from "components/Order";
import {
  AddAsset,
  UpdateAsset,
  DisplayAssets,
  AssetsBarcode,
} from "components/Asset";
import {
  AddBulkAsset,
  UpdateBulkAsset,
  DisplayBulkAssets,
  BulkAssetsBarcode,
} from "components/BulkAsset";
import DisplayNav from "./DisplayNav";

const UserNav = () => {
  const options = {
    asset: [
      {
        id: 1,
        name: "Add Asset",
        prop: AddAsset,
      },
      {
        id: 2,
        name: "Update Asset",
        prop: UpdateAsset,
      },
      {
        id: 3,
        name: "Display Assets",
        prop: DisplayAssets,
      },
      {
        id: 4,
        name: "Assets Barcode",
        prop: AssetsBarcode,
      },
    ],
    bulkAsset: [
      {
        id: 11,
        name: "Add Bulk Asset",
        prop: AddBulkAsset,
      },
      {
        id: 22,
        name: "Update Bulk Asset",
        prop: UpdateBulkAsset,
      },
      {
        id: 33,
        name: "Display Bulk Assets",
        prop: DisplayBulkAssets,
      },
      {
        id: 44,
        name: "Bulk Assets Barcode",
        prop: BulkAssetsBarcode,
      },
    ],
    order: [
      {
        id: 111,
        name: "Add Order",
        prop: AddOrder,
      },
      {
        id: 222,
        name: "Update Order",
        prop: UpdateOrder,
      },
      {
        id: 333,
        name: "Display Orders",
        prop: DisplayOrders,
      },
    ],
  };
  return <DisplayNav types={options} />;
};

export default UserNav;
