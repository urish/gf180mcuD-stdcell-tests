module tb (
    a1,
    a2,
    b,
    aoi21_1_zn
);
  input wire a1;
  input wire a2;
  input wire b;
  output wire aoi21_1_zn;

  gf180mcu_fd_sc_mcu7t5v0__aoi21_1 aoi21_1_inst (
      .A1(a1),
      .A2(a2),
      .B (b),
      .ZN(aoi21_1_zn)
  );

  // Dump the signals to a FST file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end


endmodule
