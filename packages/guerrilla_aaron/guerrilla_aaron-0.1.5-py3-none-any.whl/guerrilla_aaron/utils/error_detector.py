

def cli_error_detector(output_data: str):
    """
    Detects errors in console output.

        Args:
            output_data (str): The console output to check for errors.

        Raises:
            ValueError: If an error or message is detected in the console output.  Messages that match the rules in msg_ignoring_rules will be ignored. 
    """
    msg_ignoring_rules_of_hat = [lambda m: "]'." in m]
    msg_ignoring_rules_of_percentage = [lambda m: 'create vlan id:' in m,
                                        lambda m: 'Config file import failed' in m]
    # msg = output_data.split('\n', 1)[0]
    msg = output_data

    # print(f"======output_data '{output_data}' output_data end ======")
    # print(f"======msg '{msg}' msg end ======")
    head = msg.find('^')
    # print(f"======head of ^{head} cli_error_detector ======")
    if head != -1:
        tmp = output_data[head:]
        msg = tmp[1:tmp.find('\r')]
        for rule in msg_ignoring_rules_of_hat:
            if rule(msg):
                break
        else:
            # print(f"output_data: {output_data}\n")
            raise ValueError(f'error "{msg}" detected in console output')
    
    head = msg.find('% ')
    # print(f"======head of %{head} cli_error_detector ======")
    if head != -1:
        tmp = output_data[head:]
        msg = tmp[2:tmp.find('\r')]
        for rule in msg_ignoring_rules_of_percentage:
            if rule(msg):
                break
        else:
            raise ValueError(f'message "{msg}" detected in console output')