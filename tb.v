module tb;
  // Simple gates inputs/outputs
  // AND gates
  reg and2_a1, and2_a2;
  wire and2_z;
  reg and3_a1, and3_a2, and3_a3;
  wire and3_z;
  reg and4_a1, and4_a2, and4_a3, and4_a4;
  wire and4_z;

  // OR gates
  reg or2_a1, or2_a2;
  wire or2_z;
  reg or3_a1, or3_a2, or3_a3;
  wire or3_z;
  reg or4_a1, or4_a2, or4_a3, or4_a4;
  wire or4_z;

  // NAND gates
  reg nand2_a1, nand2_a2;
  wire nand2_zn;
  reg nand3_a1, nand3_a2, nand3_a3;
  wire nand3_zn;
  reg nand4_a1, nand4_a2, nand4_a3, nand4_a4;
  wire nand4_zn;

  // NOR gates
  reg nor2_a1, nor2_a2;
  wire nor2_zn;
  reg nor3_a1, nor3_a2, nor3_a3;
  wire nor3_zn;
  reg nor4_a1, nor4_a2, nor4_a3, nor4_a4;
  wire nor4_zn;

  // XOR gates
  reg xor2_a1, xor2_a2;
  wire xor2_z;
  reg xor3_a1, xor3_a2, xor3_a3;
  wire xor3_z;

  // XNOR gate
  reg xnor2_a1, xnor2_a2;
  wire xnor2_zn;

  // Inverter
  reg clkinv_i;
  wire clkinv_zn;

  // Multiplexer
  reg mux2_i0, mux2_i1, mux2_s;
  wire mux2_z;

  // AOI gates
  reg aoi21_a1, aoi21_a2, aoi21_b;
  wire aoi21_zn;

  reg aoi22_a1, aoi22_a2, aoi22_b1, aoi22_b2;
  wire aoi22_zn;

  reg aoi211_a1, aoi211_a2, aoi211_b, aoi211_c;
  wire aoi211_zn;

  reg aoi221_a1, aoi221_a2, aoi221_b1, aoi221_b2, aoi221_c;
  wire aoi221_zn;

  reg aoi222_a1, aoi222_a2, aoi222_b1, aoi222_b2, aoi222_c1, aoi222_c2;
  wire aoi222_zn;

  // OAI gates
  reg oai21_a1, oai21_a2, oai21_b;
  wire oai21_zn;

  reg oai22_a1, oai22_a2, oai22_b1, oai22_b2;
  wire oai22_zn;

  reg oai211_a1, oai211_a2, oai211_b, oai211_c;
  wire oai211_zn;

  reg oai221_a1, oai221_a2, oai221_b1, oai221_b2, oai221_c;
  wire oai221_zn;

  reg oai222_a1, oai222_a2, oai222_b1, oai222_b2, oai222_c1, oai222_c2;
  wire oai222_zn;

  reg oai31_a1, oai31_a2, oai31_a3, oai31_b;
  wire oai31_zn;

  reg oai32_a1, oai32_a2, oai32_a3, oai32_b1, oai32_b2;
  wire oai32_zn;

  // Gate instantiations

  // AND gates
  gf180mcu_fd_sc_mcu7t5v0__and2_1 and2_inst (
      .A1(and2_a1),
      .A2(and2_a2),
      .Z (and2_z)
  );

  gf180mcu_fd_sc_mcu7t5v0__and3_1 and3_inst (
      .A1(and3_a1),
      .A2(and3_a2),
      .A3(and3_a3),
      .Z (and3_z)
  );

  gf180mcu_fd_sc_mcu7t5v0__and4_1 and4_inst (
      .A1(and4_a1),
      .A2(and4_a2),
      .A3(and4_a3),
      .A4(and4_a4),
      .Z (and4_z)
  );

  // OR gates
  gf180mcu_fd_sc_mcu7t5v0__or2_1 or2_inst (
      .A1(or2_a1),
      .A2(or2_a2),
      .Z (or2_z)
  );

  gf180mcu_fd_sc_mcu7t5v0__or3_1 or3_inst (
      .A1(or3_a1),
      .A2(or3_a2),
      .A3(or3_a3),
      .Z (or3_z)
  );

  gf180mcu_fd_sc_mcu7t5v0__or4_1 or4_inst (
      .A1(or4_a1),
      .A2(or4_a2),
      .A3(or4_a3),
      .A4(or4_a4),
      .Z (or4_z)
  );

  // NAND gates
  gf180mcu_fd_sc_mcu7t5v0__nand2_1 nand2_inst (
      .A1(nand2_a1),
      .A2(nand2_a2),
      .ZN(nand2_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__nand3_1 nand3_inst (
      .A1(nand3_a1),
      .A2(nand3_a2),
      .A3(nand3_a3),
      .ZN(nand3_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__nand4_1 nand4_inst (
      .A1(nand4_a1),
      .A2(nand4_a2),
      .A3(nand4_a3),
      .A4(nand4_a4),
      .ZN(nand4_zn)
  );

  // NOR gates
  gf180mcu_fd_sc_mcu7t5v0__nor2_1 nor2_inst (
      .A1(nor2_a1),
      .A2(nor2_a2),
      .ZN(nor2_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__nor3_1 nor3_inst (
      .A1(nor3_a1),
      .A2(nor3_a2),
      .A3(nor3_a3),
      .ZN(nor3_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__nor4_1 nor4_inst (
      .A1(nor4_a1),
      .A2(nor4_a2),
      .A3(nor4_a3),
      .A4(nor4_a4),
      .ZN(nor4_zn)
  );

  // XOR gates
  gf180mcu_fd_sc_mcu7t5v0__xor2_1 xor2_inst (
      .A1(xor2_a1),
      .A2(xor2_a2),
      .Z (xor2_z)
  );

  gf180mcu_fd_sc_mcu7t5v0__xor3_1 xor3_inst (
      .A1(xor3_a1),
      .A2(xor3_a2),
      .A3(xor3_a3),
      .Z (xor3_z)
  );

  // XNOR gate
  gf180mcu_fd_sc_mcu7t5v0__xnor2_1 xnor2_inst (
      .A1(xnor2_a1),
      .A2(xnor2_a2),
      .ZN(xnor2_zn)
  );

  // Inverter
  gf180mcu_fd_sc_mcu7t5v0__clkinv_1 clkinv_inst (
      .I (clkinv_i),
      .ZN(clkinv_zn)
  );

  // Multiplexer
  gf180mcu_fd_sc_mcu7t5v0__mux2_2 mux2_inst (
      .I0(mux2_i0),
      .I1(mux2_i1),
      .S (mux2_s),
      .Z (mux2_z)
  );

  // AOI gates
  gf180mcu_fd_sc_mcu7t5v0__aoi21_1 aoi21_inst (
      .A1(aoi21_a1),
      .A2(aoi21_a2),
      .B (aoi21_b),
      .ZN(aoi21_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__aoi22_1 aoi22_inst (
      .A1(aoi22_a1),
      .A2(aoi22_a2),
      .B1(aoi22_b1),
      .B2(aoi22_b2),
      .ZN(aoi22_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__aoi211_1 aoi211_inst (
      .A1(aoi211_a1),
      .A2(aoi211_a2),
      .B (aoi211_b),
      .C (aoi211_c),
      .ZN(aoi211_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__aoi221_1 aoi221_inst (
      .A1(aoi221_a1),
      .A2(aoi221_a2),
      .B1(aoi221_b1),
      .B2(aoi221_b2),
      .C (aoi221_c),
      .ZN(aoi221_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__aoi222_1 aoi222_inst (
      .A1(aoi222_a1),
      .A2(aoi222_a2),
      .B1(aoi222_b1),
      .B2(aoi222_b2),
      .C1(aoi222_c1),
      .C2(aoi222_c2),
      .ZN(aoi222_zn)
  );

  // OAI gates
  gf180mcu_fd_sc_mcu7t5v0__oai21_1 oai21_inst (
      .A1(oai21_a1),
      .A2(oai21_a2),
      .B (oai21_b),
      .ZN(oai21_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__oai22_1 oai22_inst (
      .A1(oai22_a1),
      .A2(oai22_a2),
      .B1(oai22_b1),
      .B2(oai22_b2),
      .ZN(oai22_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__oai211_1 oai211_inst (
      .A1(oai211_a1),
      .A2(oai211_a2),
      .B (oai211_b),
      .C (oai211_c),
      .ZN(oai211_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__oai221_1 oai221_inst (
      .A1(oai221_a1),
      .A2(oai221_a2),
      .B1(oai221_b1),
      .B2(oai221_b2),
      .C (oai221_c),
      .ZN(oai221_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__oai222_1 oai222_inst (
      .A1(oai222_a1),
      .A2(oai222_a2),
      .B1(oai222_b1),
      .B2(oai222_b2),
      .C1(oai222_c1),
      .C2(oai222_c2),
      .ZN(oai222_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__oai31_1 oai31_inst (
      .A1(oai31_a1),
      .A2(oai31_a2),
      .A3(oai31_a3),
      .B (oai31_b),
      .ZN(oai31_zn)
  );

  gf180mcu_fd_sc_mcu7t5v0__oai32_1 oai32_inst (
      .A1(oai32_a1),
      .A2(oai32_a2),
      .A3(oai32_a3),
      .B1(oai32_b1),
      .B2(oai32_b2),
      .ZN(oai32_zn)
  );

  // Dump the signals to a VCD file
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

endmodule
