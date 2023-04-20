import React, { useContext, useRef } from "react";
import Form from "components/Form";
import DataTable from "components/Table"

export const AddBulkAsset = () => {
  const date = new Date();
  const year = date.getFullYear();
  const fields = [
    { type: "text", id: "asset_name", required: true, label: "Asset Name" },
    { type: "text", id: "model", required: false, label: "Model" },
    { type: "text", id: "asset_make", required: false, label: "Asset Make" },
    { type: "text", id: "serial_no", required: true, label: "Serial No" },
    {
      type: "text",
      id: "department",
      required: false,
      label: "Department",
    },
    {
      type: "text",
      id: "asset_location",
      required: false,
      label: "Asset Location",
    },
    {
      type: "select",
      id: "asset_type",
      required: false,
      label: "Asset Type",
      options: [
        { value: "consumable", label: "Consumable" },
        { value: "non_consumable", label: "Non Consumable" },
      ],
    },
    { type: "date", id: "entry_date", required: false, label: "Entry Date" },
    { type: "number", id: "quantity", required: false, label: "Quantity", min: 0, },
    {
      type: "text",
      id: "purchase_order_no",
      required: true,
      label: "Purchase Order No",
    },
    {
      type: "number",
      id: "financial_year",
      required: true,
      step: "1",
      min: 2000,
      currentYear: year,
      label: "Financial Year",
    },
    {
      type: "select",
      id: "asset_state",
      required: false,
      label: "Asset State",
      options: [
        { value: "in_use", label: "In Use" },
        { value: "in_store", label: "In Store" },
        { value: "sold", label: "Sold" },
      ],
    },
    { type: "image", id: "picture", required: false, label: "Picture" },
  ];
  const apiLink = "http://localhost:8000/add-bulk-asset";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"POST"}
        submitName={"Add Bulk Asset"}
        headers={{
          "Content-Type": "multipart/form-data",
        }}
      />
    </>
  );
};

export const DeleteBulkAsset = () => {
  const fields = [
    { type: "text", id: "serial_no", required: true, label: "Serial No" },
    { type: "text", id: "asset_location", required: true, label: "Asset Location" },

  ];
  const apiLink = "http://localhost:8000/delete-bulk-asset/${serial_no}/${asset_location}";

  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"DELETE"}
        submitName={"Delete Bulk Asset"}
      />
    </>
  );
};

export const UpdateBulkAsset = () => {
  const date = new Date();
  const year = date.getFullYear();
  const fields = [
    { type: "text", id: "serial_no", required: true, label: "Serial No" },
    { type: "text", id: "asset_name", required: false, label: "Asset Name" },
    { type: "text", id: "model", required: false, label: "Model" },
    { type: "text", id: "asset_make", required: false, label: "Asset Make" },
    {
      type: "text",
      id: "department",
      required: false,
      label: "Department",
    },
    {
      type: "text",
      id: "asset_location",
      required: false,
      label: "Asset Location",
    },
    {
      type: "text",
      id: "asset_holder",
      required: false,
      label: "Asset Holder",
    },
    {
      type: "select",
      id: "asset_type",
      required: false,
      label: "Asset Type",
      options: [
        { value: "", label: "Select" },
        { value: "consumable", label: "Consumable" },
        { value: "non_consumable", label: "Non Consumable" },
      ],
    },
    { type: "date", id: "entry_date", required: false, label: "Entry Date" },
    { type: "number", id: "quantity", required: false, label: "Quantity" },
    // { type: "date", id: "warranty", required: false, label: "Warranty" },
    {
      type: "text",
      id: "purchase_order_no",
      required: false,
      label: "Purchase Order No",
    },
    {
      type: "number",
      id: "financial_year",
      required: false,
      step: "1",
      min: 2000,
      currentYear: year,
      label: "Financial Year",
    },
    {
      type: "select",
      id: "asset_state",
      required: false,
      label: "Asset State",
      options: [
        { value: "", label: "Select" },
        { value: "in_use", label: "In Use" },
        { value: "in_store", label: "In Store" },
        { value: "sold", label: "Sold" },
      ],
    },
    { type: "image", id: "picture", required: false, label: "Picture" },
  ];

  const apiLink = "http://localhost:8000/update-bulk-asset";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"PUT"}
        submitName={"Update Bulk Asset"}
        headers={{
          "Content-Type": "multipart/form-data",
        }}
      />
    </>
  );
};

export const DisplayBulkAssets = () => {
  const apiLink = "http://localhost:8000/get-all-bulk-asset";

  return (
    <>
    <DataTable
      apiLink={apiLink}
      method={"GET"}
      tableName={"All Bulk Assets"}
    />
    </>
  )
}
