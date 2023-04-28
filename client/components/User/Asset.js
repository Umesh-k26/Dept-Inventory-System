import React, { useContext, useRef } from "react";
import { Form } from "components/Form";
import DataTable from "components/Table";
import { BarcodeGenerator } from "components/Barcode";

export const AddAsset = () => {
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
    { type: "text", id: "asset_holder", required: true, label: "Asset Holder" },
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
    { type: "date", id: "warranty", required: false, label: "Warranty" },
    {
      type: "select",
      id: "is_hardware",
      required: false,
      label: "Hardware",
      options: [
        { value: "false", label: "No" },
        { value: "true", label: "Yes" },
      ],
    },
    { type: "text", id: "system_no", required: false, label: "System No" },
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
  const apiLink = "http://localhost:8000/add-asset";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"POST"}
        submitName={"Add Asset"}
        headers={{
          "Content-Type": "multipart/form-data",
        }}
      />
    </>
  );
};

export const DeleteAsset = () => {
  const fields = [
    { type: "text", id: "serial_no", required: true, label: "Serial No" },
  ];
  const apiLink = "http://localhost:8000/delete-asset/${serial_no}";

  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"DELETE"}
        submitName={"Delete Asset"}
      />
    </>
  );
};

export const UpdateAsset = () => {
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
    { type: "date", id: "warranty", required: false, label: "Warranty" },
    {
      type: "select",
      id: "is_hardware",
      required: false,
      label: "Hardware",
      options: [
        { value: "", label: "Select" },
        { value: "false", label: "No" },
        { value: "true", label: "Yes" },
      ],
    },
    { type: "text", id: "system_no", required: false, label: "System No" },
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

  const apiLink = "http://localhost:8000/update-asset";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"PUT"}
        submitName={"Update Asset"}
        headers={{
          "Content-Type": "multipart/form-data",
        }}
      />
    </>
  );
};

export const DisplayAssets = () => {
  const apiLink = "http://localhost:8000/get-all-asset";

  return (
    <>
      <DataTable apiLink={apiLink} method={"GET"} tableName={"All Assets"} />
    </>
  );
};

export const AssetsBarcode = () => {
  const date = new Date();
  const year = date.getFullYear();
  const fields = [
    { type: "text", id: "serial_no", required: false, label: "Serial No" },
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
    { type: "date", id: "warranty", required: false, label: "Warranty" },
    {
      type: "select",
      id: "is_hardware",
      required: false,
      label: "Hardware",
      options: [
        { value: "", label: "Select" },
        { value: "false", label: "No" },
        { value: "true", label: "Yes" },
      ],
    },
    { type: "text", id: "system_no", required: false, label: "System No" },
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
  ];

  const apiLink = "http://localhost:8000/get-asset";

  return (
    <>
      <BarcodeGenerator
        fields={fields}
        apiLink={apiLink}
        method={"POST"}
        submitName={"Generate Barcode"}
      />
    </>
  );
};
// export const AllAssets = () => {};
// export const AddAsset = () => {
//   const baseURL = process.env.REACT_APP_API_BASEURL;
//   console.log(baseURL);
//   const assetName = useRef(null);
//   const assetModel = useRef(null);
//   const serialNo = useRef(null);
//   const assetDepartment = useRef(null);
//   const assetLocation = useRef(null);
//   const assetHolder = useRef(null);
//   const entryDate = useRef(null);
//   const unitPrice = useRef(null);
//   const assetWarranty = useRef(null);
//   const isHardware = useRef(null);
//   const systemNo = useRef(null);
//   const purchaseOrderNo = useRef(null);
//   const assetState = useRef(null);
//   const assetPicture = useRef(null);

//   const addAsset = async (event) => {
//     event.preventDefault();

//     const res = await fetch(`http://localhost:8000/add-asset`, {
//       method: "POST",
//       body: JSON.stringify({
//         asset_name: assetName.current.value,
//         model: assetModel.current.value,
//         serial_no: serialNo.current.value,
//         asset_department: assetDepartment.current.value,
//         asset_location: assetLocation.current.value,
//         asset_holder: assetHolder.current.value,
//         entry_date: entryDate.current.value == "" ? null : entryDate.current.value,
//         unit_price: unitPrice.current.value == "" ? null : unitPrice.current.value,
//         warranty: assetWarranty.current.value == "" ? null : assetWarranty.current.value,
//         is_hardware: isHardware.current.value == "" ? null : isHardware.current.value,
//         system_no: systemNo.current.value,
//         purchase_order_no: purchaseOrderNo.current.value,
//         asset_state: assetState.current.value,
//         picture: assetPicture.current.value,

//       }),
//       headers: {
//         "Content-Type": "application/json",
//       },
//     });
//     const data = res.json();
//     console.log(data);
//   };
//   return (
//     <>
//       <div className="container flex">
//         <form onSubmit={addAsset}>
//           <label htmlFor="asset_name">Asset Name</label>
//           <input type="text" id="asset_name" ref={assetName}  />
//           <label htmlFor="serial_no">Serial Number</label>
//           <input type="text" id="serial_no" ref={serialNo}  required/>
//           <label htmlFor="model">Model</label>
//           <input type="text" id="model" ref={assetModel} />
//           <label htmlFor="department">Department</label>
//           <input type="text" id="department" ref={assetDepartment}  />
//           <label htmlFor="asset_location">Asset Location</label>
//           <input type="text" id="asset_location" ref={assetLocation} />
//           <label htmlFor="asset_holder">Asset Holder</label>
//           <input type="text" id="asset_holder" ref={assetHolder} />
//           <label htmlFor="entry_date">Entry Date</label>
//           <input type="date" id="entry_date" ref={entryDate} />
//           <label htmlFor="unit_price">Unit Price</label>
//           <input type="number" id="unit_price" ref={unitPrice} />
//           <label htmlFor="warranty">Warranty</label>
//           <input type="date" id="warranty" ref={assetWarranty} />
//           <label htmlFor="is_hardware">Hardware</label>
//           <input type="text" id="is_hardware" ref={isHardware} />
//           <label htmlFor="system_no">System Number</label>
//           <input type="text" id="system_no" ref={systemNo} />
//           <label htmlFor="purchase_order_no">Purchase Order No.</label>
//           <input type="text" id="purchase_order_no" ref={purchaseOrderNo} />
//           <label htmlFor="asset_state">Asset State</label>
//           <input type="text" id="asset_state" ref={assetState} />
//           <label htmlFor="picture">Picture</label>
//           <input type="text" id="picture" ref={assetPicture} />

//           <button type="submit">Add Asset</button>
//         </form>
//       </div>
//     </>
//   );
// };
