import React, { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import MUIDataTable from "mui-datatables";

const options = {
  filterType: "dropdown",
  download: true,
  print: true,
  selectableRows: "multiple",
  responsive: "simple",
  // overFlowX: "auto",
  selectableRows: "none",
  downloadOptions: {
    filterOptions: {
      useDisplayedColumnsOnly: true,
      useDisplayedRowsOnly: true,
    },
  },
};

export const DataTable = ({ apiLink, method, tableName, customRender }) => {
  const { data: session, status } = useSession();
  let columns = [];

  const [tableData, setTableData] = useState();

  useEffect(() => {
    const getData = async () => {
      const res = await fetch(apiLink, {
        method: method,
        headers: {
          Authorization: session.accessToken,
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      setTableData(data);
    };
    getData();
    console.log(tableData);
  }, []);

  if (tableData) {
    customRender = { ...customRender };
    tableData.column_name.forEach((col) => {
      columns.push({
        name: col,
        options: {
          filter: true,
          sort: true,
          setCellProps: (value) => {
            return {
              style: {
                whiteSpace: "normal",
                // height: "auto",
                innerWidth: "auto",
                outerWidth: "auto",
                overFlowX: "hidden",
                wordwrap: true,
              },
            };
          },
          customBodyRender: customRender[col],
        },
      });
    });

    return (
      <>
        <MUIDataTable
          title={tableName}
          columns={columns}
          data={tableData.values}
          options={options}
        />
      </>
    );
  }
};

export default DataTable;
