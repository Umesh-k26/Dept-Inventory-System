import { getSession } from "next-auth/react";
import React, { useContext, useRef } from "react";

export const AddOrder = () => {
  const baseURL = process.env.REACT_APP_API_BASEURL;
  console.log(baseURL);
  const purchaseOrderNo = useRef(null);
  const orderDate = useRef(null);
  const Indentor = useRef(null);
  const firmName = useRef(null);
  const financialYear = useRef(null);
  const gstTin = useRef(null);
  const finalProcurementDate = useRef(null);
  const invoiceNo = useRef(null);
  const invoiceDate = useRef(null);


  const addOrder = async (event) => {
    event.preventDefault();

    const res = await fetch(`http://localhost:8000/add-order`, {
      method: "POST",
      body: JSON.stringify({
        purchase_order_no: purchaseOrderNo.current.value,
        order_date: orderDate.current.value == "" ? null : orderDate.current.value,
        indentor: Indentor.current.value,
        firm_name: firmName.current.value,
        financial_year: financialYear.current.value == "" ? null : financialYear.current.value,
        gst_tin: gstTin.current.value,
        final_procurement_date: finalProcurementDate.current.value == "" ? null : finalProcurementDate.current.value,
        invoice_no: invoiceNo.current.value,
        invoiceDate: invoiceDate.current.value == "" ? null : invoiceDate.current.value,


      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = res.json();
    console.log(data);
  };
  return (
    <>
      <div className="container flex">
        <form onSubmit={addOrder}>
          <label htmlFor="purchase_order_no">Purchase Order Num</label>
          <input type="text" id="purchase_order_no" ref={purchaseOrderNo}  required/>
          <label htmlFor="order_date">Order Date</label>
          <input type="date" id="order_date" ref={orderDate} />
          <label htmlFor="indentor">Indentor</label>
          <input type="text" id="indentor" ref={Indentor} required/>
          <label htmlFor="firm_name">Firm Name</label>
          <input type="text" id="firm_name" ref={firmName}  />
          <label htmlFor="financial_year">Financial Year</label>
          <input type="number" id="financial_year" ref={financialYear}  />
          <label htmlFor="gst_tin">GST TIN</label>
          <input type="text" id="gst_tin" ref={gstTin} />
          <label htmlFor="final_procurement_date">Final Procurement Date</label>
          <input type="date" id="final_procurement_date" ref={finalProcurementDate} />
          <label htmlFor="invoice_no">Invoice No</label>
          <input type="text" id="invoice_no" ref={invoiceNo} required/>
          <label htmlFor="invoice_date">Invoice Date</label>
          <input type="date" id="invoice_date" ref={invoiceDate} />

          <button type="submit">Add Order</button>
        </form>
      </div>
    </>
  );
};
