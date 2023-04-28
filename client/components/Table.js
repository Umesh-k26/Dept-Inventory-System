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

export const DataTable = ({ apiLink, method, tableName }) => {
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
  },[]);

  if (tableData) {
    console.log(tableData);
    
    for (let i = 0; i < tableData.column_name.length; i++) {
      if(tableData.column_name[i] == "serial_no")
      {
        if(tableName == "All Assets")
        {
          columns.push({
            name: tableData.column_name[i],
              options: {
                filter: true,
                sort: true,
                customBodyRender: (value) => (
                  <a href={"http://localhost:8000/files/assets/"+ String(value) + '.png'} target="_blank"> {value} </a>
                ),
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
              },
          })
        }
        else if(tableName == "All Bulk Assets"){
          columns.push({
            name: tableData.column_name[i],
              options: {
                filter: true,
                sort: true,
                customBodyRender: (value) => (
                  <a href={"http://localhost:8000/files/bulk_assets/"+ String(value) + '.png'} target="_blank"> {value} </a>
                ),
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
              },
          })
        }
      }
      else{
        columns.push({
          name: tableData.column_name[i],
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
          },
        });
      }
    }

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
