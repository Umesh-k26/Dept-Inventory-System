import React, { useContext, useRef } from "react";
import Form from "components/Form";

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
  ];
  const apiLink = "http://localhost:8000/add-order";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"POST"}
        submitName={"Add Order"}
        // headers={{
        //   "Content-Type": "application/json",
        // }}
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
  ];
  const apiLink = "http://localhost:8000/update-order";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"PUT"}
        submitName={"Update Order"}
      />
    </>
  );
};

// export const AddOrder = () => {
//   const baseURL = process.env.REACT_APP_API_BASEURL;
//   console.log(baseURL);
//   const purchaseOrderNo = useRef(null);
//   const orderDate = useRef(null);
//   const Indentor = useRef(null);
//   const firmName = useRef(null);
//   const financialYear = useRef(null);
//   const gstTin = useRef(null);
//   const finalProcurementDate = useRef(null);
//   const invoiceNo = useRef(null);
//   const invoiceDate = useRef(null);

//   const addOrder = async (event) => {
//     event.preventDefault();

//     const res = await fetch(`http://localhost:8000/add-order`, {
//       method: "POST",
//       body: JSON.stringify({
//         purchase_order_no: purchaseOrderNo.current.value,
//         order_date: orderDate.current.value == "" ? null : orderDate.current.value,
//         indentor: Indentor.current.value,
//         firm_name: firmName.current.value,
//         financial_year: financialYear.current.value == "" ? null : financialYear.current.value,
//         gst_tin: gstTin.current.value,
//         final_procurement_date: finalProcurementDate.current.value == "" ? null : finalProcurementDate.current.value,
//         invoice_no: invoiceNo.current.value,
//         invoice_date: invoiceDate.current.value == "" ? null : invoiceDate.current.value,

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
//         <form onSubmit={addOrder}>
//           <label htmlFor="purchase_order_no">Purchase Order Num</label>
//           <input type="text" id="purchase_order_no" ref={purchaseOrderNo}  required/>
//           <label htmlFor="order_date">Order Date</label>
//           <input type="date" id="order_date" ref={orderDate} />
//           <label htmlFor="indentor">Indentor</label>
//           <input type="text" id="indentor" ref={Indentor} required/>
//           <label htmlFor="firm_name">Firm Name</label>
//           <input type="text" id="firm_name" ref={firmName}  />
//           <label htmlFor="financial_year">Financial Year</label>
//           <input type="number" id="financial_year" ref={financialYear}  />
//           <label htmlFor="gst_tin">GST TIN</label>
//           <input type="text" id="gst_tin" ref={gstTin} />
//           <label htmlFor="final_procurement_date">Final Procurement Date</label>
//           <input type="date" id="final_procurement_date" ref={finalProcurementDate} />
//           <label htmlFor="invoice_no">Invoice No</label>
//           <input type="text" id="invoice_no" ref={invoiceNo} required/>
//           <label htmlFor="invoice_date">Invoice Date</label>
//           <input type="date" id="invoice_date" ref={invoiceDate} />

//           <button type="submit">Add Order</button>
//         </form>
//       </div>
//     </>
//   );
// };

// export const DeleteOrder = () => {
//     const purchaseOrderNo = useRef(null);
//     const invoiceNo = useRef(null);

//     const deleteOrder = async () => {
//       const res = await fetch(`http://localhost:8000/${purchaseOrderNo}${invoiceNo}`, {
//         method: "DELETE",
//         headers: {
//           "Content-Type": "application/json",
//         },
//       });
//     };
//     return (
//       <>
//         <div>
//           <form onSubmit={deleteOrder}>
//             <label htmlFor="purchase_order_no">Purchase Order No</label>
//             <input type="text" id="purchase_order_no" ref={purchaseOrderNo} required />

//             <label htmlFor="invoice_no">Invoice No</label>
//             <input type="text" id="invoice_no" ref={invoiceNo} required />

//             <button type="submit">Delete Order</button>
//           </form>
//         </div>
//       </>
//     );
//   };
