import os

def generate_uvm_testbench():
    """
    Script to generate a complete UVM testbench with separate files for each component.
    """
    module_name = input("Enter the name of the module: ").strip()
    num_agents = int(input("Enter the number of agents: ").strip())

    agents = []
    for i in range(num_agents):
        print(f"\nAgent {i + 1}:")
        agent_name = input("  Enter the agent name: ").strip()
        agent_type = input("  Enter the agent type (e.g., master/slave): ").strip()
        agents.append((agent_name, agent_type))

    base_dir = f"{module_name}_tb"

    # Create directory structure
    directories = ["rtl", "tb", "sim", "tests"]
    for dir_name in directories:
        os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)

    # Generate agent components
    for agent_name, _ in agents:
        driver_class_name = f"{module_name}_{agent_name}_driver"
        monitor_class_name = f"{module_name}_{agent_name}_monitor"
        sequencer_class_name = f"{module_name}_{agent_name}_sequencer"
        transaction_class_name = f"{module_name}_{agent_name}_transaction"
        sequence_class_name = f"{module_name}_{agent_name}_sequence"
        agent_interface_name = f"{module_name}_{agent_name}_interface"
        agent_class_name = f"{module_name}_{agent_name}_agent"
        agent_Config_name = f"{module_name}_{agent_name}_agentConfig"


        #agentfile
        file_path = os.path.join(base_dir, "tb", f"{agent_class_name}.sv")
        with open(file_path,"w") as f:
            f.write(f"class {agent_class_name} extends uvm_agent;\n")
            f.write(f"`uvm_component_utils({agent_class_name})\n\n")
            f.write("//instantiating agent components\n\n")
            f.write(f"{driver_class_name} {agent_name}_driver;\n")
            f.write(f"{monitor_class_name} {agent_name}_monitor;\n")
            f.write(f"{sequencer_class_name} {agent_name}_sequencer;\n\n")
            f.write(f"{agent_Config_name} {agent_name}_agentConfig;\n")
            f.write(f'function new(string name = "{agent_class_name}", uvm_component parent);\n'
                    " super.new(name,parent);\n"
                    "endfunction\n"
                    "//build phase\n"
                    "function void build_phase(uvm_phase phase);\n"
                    " super.build_phase(phase);\n"
                    f' if(!uvm_config_db #({agent_Config_name})::get(this,"","{agent_Config_name}",{agent_name}_agentConfig))\n'
                    f'  `uvm_fatal("{agent_class_name}",Not able to get config have you set it??)\n'
                    f' {agent_name}_monitor = {monitor_class_name}::type_id::create("{agent_name}_monitor",this);\n\n'
                    f' if({agent_name}_agentConfig.is_active == UVM_ACTIVE)\n'
                    " begin\n"
                    f'   {agent_name}_driver = {driver_class_name}::type_id::create("{agent_name}_driver",this);\n'
                    f'   {agent_name}_sequencer = {sequencer_class_name}::type_id::create("{agent_name}_sequencer",this);\n'
                    " end\n"
                    " else\n"
                    f'   `uvm_info("{agent_class_name}", "Agent is UVM_PASSIVE",UVM_NONE)\n'
                    "endfunction\n"
                    "function void connect_phase(uvm_phase phase)\n"
                    f' if({agent_name}_agentConfig.is_active = UVM_ACTIVE)\n'
                    f'  {agent_name}_driver.seq_item_port.connect({agent_name}_sequencer.seq_item_export);\n'
                    "endfunction\n")
            f.write("endclass\n")
        
        #agentCOnfig file
        file_path = os.path.join(base_dir, "tb" , f"{agent_Config_name}.sv")
        with open(file_path,"w") as f:
            f.write(f"class {agent_Config_name} extends uvm_object;\n"
                    " //registering with factory\n"
                    f" `uvm_object_utils({agent_Config_name})\n"
                    " //Config parameters\n"
                    " uvm_active_passive_enum is_active = UVM_PASSIVE;\n"
                    f'function new(string name = {agent_Config_name});\n'
                    "super.new(name)\n"
                    "endfunction\n"
                    "endclass" )
        #driver
        file_path = os.path.join(base_dir, "tb" , f"{driver_class_name}.sv")
        with open(file_path,"w") as f:
            f.write(f'class {driver_class_name} extends uvm_driver#({transaction_class_name});\n'
                    "//registering with factory\n"
	                f' `uvm_component_utils({driver_class_name})\n'
	                "//virtual interface\n"
	                f'virtual {agent_interface_name} {agent_name}_intf;\n'
	                f'virtual {agent_interface_name}.drv_mod vif;\n'
	                f'function new(string name = "{driver_class_name}", uvm_component parent);\n'
                    " super.new(name,parent);\n"
                    "endfunction\n"
                    "function void build_phase(uvm_phase phase);\n"
                    " super.build_phase(phase);\n"
                    f' if(!uvm_config_db #(virtual {agent_interface_name})::get(uvm_root::get(),"*","{agent_interface_name}",{agent_name}_intf))\n'
                    f'  `uvm_fatal("{driver_class_name}","Not able to get agent_interface have you set it??")\n'
                    "endfunction\n"
                    "function void connect_phase(uvm_phase phase);\n"
                    "//connect driver virtual interface with modport and virtual interface from config db\n"
                    f'  vif = {agent_name}_intf;\n'
                    "endfunction\n"
                    "task run_phase(uvm_phase phase);\n"
                    " wait(vif.pi_rst_n);\n"
                    " @(vif.drv_cb);\n"
                    " wait(vif.pi_rst_n);\n"
                    " wait(vif.pi_rst_n);\n"
                    "forever\n"
                    "    begin\n"
                    "    //get seq item\n"
                    "    seq_item_port.get_next_item(req);\n"
                    "    sent_to_dut(req);\n"
                    "    seq_item_port.item_done();\n"	
                    "    end\n"
                    "endtask\n"
                    f'task sent_to_dut({transaction_class_name} sequence_item);\n'
                    "//write the driver logic\n"
                    "endtask\n"
                    "endclass\n"	)
            
        #monitor file
        file_path = os.path.join(base_dir, "tb", f"{monitor_class_name}.sv")
        with open(file_path,"w") as f:
            f.write(f'class {monitor_class_name} extends uvm_monitor;\n'
                    "//registering with factory\n"
	                f' `uvm_component_utils({monitor_class_name})\n'
                    f' {transaction_class_name} seq_item;\n'
	                "//virtual interface\n"
	                f' virtual {agent_interface_name} {agent_name}_intf;\n'
	                f' virtual {agent_interface_name}.mon_mod vif;\n'
                    f'  uvm_analysis_port #({transaction_class_name}) monitor_port;\n'
	                f'function new(string name = "{monitor_class_name}", uvm_component parent);\n'
                    " super.new(name,parent);\n"
                    'monitor_port = new("monitor_port",this);\n'
                    "endfunction\n"
                    "function void build_phase(uvm_phase phase);\n"
                    " super.build_phase(phase);\n"
                    f' if(!uvm_config_db #(virtual {agent_interface_name})::get(uvm_root::get(),"*","{agent_interface_name}",{agent_name}_intf))\n'
                    f'  `uvm_fatal("{monitor_class_name}","Not able to get agent_interface have you set it??")\n'
                    "endfunction\n"
                    "function void connect_phase(uvm_phase phase);\n"
                    "//connect driver virtual interface with modport and virtual interface from config db\n"
                    f'  vif = {agent_name}_intf;\n'
                    "endfunction\n"
                    "task run_phase(uvm_phase phase);\n"
                    "forever collect_data();\n"
                    "endtask\n"
                    f'task collect_data();\n'
                    "//write the driver logic\n"
                    f' seq_item = {transaction_class_name}::type_id::create("seq_item");\n'
                    " @(vif.mon_cb)\n"
                    "monitor_port.write(seq_item)\n"
                    "endtask\n"
                    "endclass\n"	)


        #interface file
        file_path = os.path.join(base_dir, "tb", f"{agent_interface_name}.sv")
        with open(file_path,"w") as f:
            f.write(f"interface {agent_interface_name} (input bit pi_clk,pi_rst_n);\n\n")
            f.write("//variables\n")
            f.write("clocking drv_cb@(posedge pi_clk)\n")
            f.write("//default input #1 output #1\n")
            f.write("//write the signals needed for driver\n")
            f.write("endclocking\n")
            f.write("clocking mon_cb@(posedge pi_clk)\n")
            f.write("//default input #1 output #1\n")
            f.write("//write the signals needed for monitor\n")
            f.write("endclocking\n\n\n")
            f.write("modport drv_mod(clocking drv_cb,input pi_rst_n)\n")
            f.write("modport mon_mod(clocking mon_cb,input pi_rst_n)\n")
            f.write("endinterface")
 

       

    print(f"\nUVM testbench for module '{module_name}' has been generated in the directory '{base_dir}'.")

if __name__ == "__main__":
    generate_uvm_testbench()