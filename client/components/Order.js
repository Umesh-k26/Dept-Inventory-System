import React, { useContext, useRef } from "react";
import { Form } from "components/Form";
import DataTable from "components/Table";

export const AddOrder = () => {
  const date = new Date();
  const year = date.getFullYear();
  const fields = [
    {
      type: "text",
      id: "purchase_order_no",
      required: true,
      label: "Purchase Order No",
    },
    { type: "date", id: "order_date", required: false, label: "Order Date" },
    { type: "text", id: "indentor", required: true, label: "Indentor" },
    { type: "text", id: "firm_name", required: false, label: "Firm Name" },
    {
      type: "number",
      id: "financial_year",
      required: true,
      label: "Financial Year",
      min: 2000,
      currentYear: year,
    },
    // { type: "text", id: "gst_tin", required: false, label: "GST TIN" },
    {
      type: "date",
      id: "final_procurement_date",
      required: false,
      label: "Final Procurement Date",
    },
    { type: "text", id: "invoice_no", required: false, label: "Invoice No" },
    {
      type: "date",
      id: "invoice_date",
      required: false,
      label: "Invoice Date",
    },
    {
      type: "number",
      id: "total_price",
      required: false,
      step: "0.01",
      min: 0,
      label: "Total Price",
    },
    {
      type: "select",
      id: "source_of_fund",
      required: false,
      label: "Source Of Fund",
      options: [
        { value: "project", label: "Project" },
        { value: "institute", label: "Institute" },
        { value: "both", label: "Both" },
      ],
    },
    {
      type: "text",
      id: "fund_info",
      required: false,
      label: "Fund Information",
    },
    {
      type: "text",
      id: "other_details",
      required: false,
      label: "Other Details",
    },
    {
      type: "file",
      id: "invoice",
      required: false,
      label: "Invoice",
      accept: "application/pdf",
    },
    {
      type: "file",
      id: "purchase_order",
      required: false,
      label: "Purchase Order",
      accept: "application/pdf",
    },
  ];
  const apiLink = "http://localhost:8000/add-order";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"POST"}
        submitName={"Add Order"}
        headers={{
          "Content-Type": "multipart/form-data",
        }}
      />
    </>
  );
};

export const DeleteOrder = () => {
  const fields = [
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
      label: "Financial Year",
    },
  ];
  const apiLink =
    "http://localhost:8000/delete-order/${purchase_order_no}/${financial_year}";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"DELETE"}
        submitName={"Delete Order"}
      />
    </>
  );
};

export const UpdateOrder = () => {
  const date = new Date();
  const year = date.getFullYear();
  const fields = [
    {
      type: "text",
      id: "purchase_order_no",
      required: true,
      label: "Purchase Order No",
    },
    { type: "date", id: "order_date", required: false, label: "Order Date" },
    { type: "text", id: "indentor", required: false, label: "Indentor" },
    { type: "text", id: "firm_name", required: false, label: "Firm Name" },
    {
      type: "number",
      id: "financial_year",
      required: true,
      label: "Financial Year",
      min: 2000,
      currentYear: year,
    },
    // { type: "text", id: "gst_tin", required: false, label: "GST TIN" },
    {
      type: "date",
      id: "final_procurement_date",
      required: false,
      label: "Final Procurement Date",
    },
    { type: "text", id: "invoice_no", required: false, label: "Invoice No" },
    {
      type: "date",
      id: "invoice_date",
      required: false,
      label: "Invoice Date",
    },
    {
      type: "number",
      id: "total_price",
      step: "0.01",
      min: 0,
      required: false,
      label: "Total Price",
    },
    {
      type: "select",
      id: "source_of_fund",
      required: false,
      label: "Source Of Fund",
      options: [
        { value: "", label: "Select" },
        { value: "project", label: "Project" },
        { value: "institute", label: "Institute" },
        { value: "both", label: "Both" },
      ],
    },
    {
      type: "text",
      id: "fund_info",
      required: false,
      label: "Fund Information",
    },
    {
      type: "text",
      id: "other_details",
      required: false,
      label: "Other Details",
    },
    {
      type: "file",
      id: "invoice",
      required: false,
      label: "Invoice",
      accept: "application/pdf",
    },
    {
      type: "file",
      id: "purchase_order",
      required: false,
      label: "Purchase Order",
      accept: "application/pdf",
    },
  ];
  const apiLink = "http://localhost:8000/update-order";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"PUT"}
        submitName={"Update Order"}
        headers={{
          "Content-Type": "multipart/form-data",
        }}
      />
    </>
  );
};

export const DisplayOrders = () => {
  const apiLink = "http://localhost:8000/get-all-order";
  const customRender = {
    purchase_order_no: (value, tableMeta, updateValue) => {
      const financialYear = tableMeta.rowData[4];
      return (
        <a
          href={`http://localhost:8000/files/purchase_order/${financialYear}_${value}.pdf`}
          target="_blank"
          className="text-red-500 hover:text-red-600 underline"
        >
          {" "}
          {value}{" "}
        </a>
      );
    },
    invoice_no: (value, tableMeta, updateValue) => {
      const purchaseOrderNo = tableMeta.rowData[0];
      const financialYear = tableMeta.rowData[4];
      return (
        <a
          href={`http://localhost:8000/files/invoices/${financialYear}_${purchaseOrderNo}.pdf`}
          target="_blank"
          className="text-red-500 hover:text-red-600 underline"
        >
          {" "}
          {value}{" "}
        </a>
      );
    },
  };
  return (
    <>
      <DataTable
        apiLink={apiLink}
        method={"GET"}
        tableName={"All Orders"}
        customRender={customRender}
      />
    </>
  );
};
