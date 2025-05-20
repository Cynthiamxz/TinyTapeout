/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.

  // 8-bit counter
  reg [7:0] counter;
  wire load           = ui_in[7];
  wire enable         = ui_in[6];
  wire dir_up         = ui_in[5];
  wire output_en      = ui_in[4];
  wire [3:0] load_val = ui_in[3:0];

  assign uio_oe = output_en ? 8'b11111111 : 8'b0; // Enable the output if output_en is high
  assign uio_out = output_en ? counter : 8'bZ; // Output the counter value if output_en is high
  assign uo_out  = counter;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      counter <= 8'b0;
    end else if (load) begin 
      counter <= { 4'b0000, load_val }; // Load value from ui_in
    end else if (enable) begin
      if (dir_up)
        counter <= counter + 1;
      else
        counter <= counter - 1;
    end
  end

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, 1'b0};

endmodule
