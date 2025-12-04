import React from "react";
import { Ticket } from "../types/ticketRes";

interface TicketTableProps {
  tickets: Ticket[];
}

const TicketTable: React.FC<TicketTableProps> = ({ tickets }) => {
  return (
    <table style={{ borderCollapse: "collapse", width: "100%" }}>
      <thead>
        <tr>
          <th style={{ border: "1px solid black", padding: "8px" }}>Ticket ID</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Similarity</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Resolution</th>
        </tr>
      </thead>
      <tbody>
        {tickets.map((ticket, index) => (
          <tr key={index}>
            <td style={{ border: "1px solid black", padding: "8px" }}>{ticket.ticketId}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{ticket.similarity}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{ticket.resolution}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TicketTable;