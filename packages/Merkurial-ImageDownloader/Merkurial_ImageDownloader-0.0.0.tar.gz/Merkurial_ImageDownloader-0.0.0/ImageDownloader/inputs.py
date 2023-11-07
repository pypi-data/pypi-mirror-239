

class TakeInput:
    start_text = "Begin"
    end_text = "Stop"
    stop_text_items = ["e", "c", "q"]

    def __init__(self, total_num_items: int, start_num: int | None = None, stop_num: int | None = None):
        self.total_num_items = total_num_items
        self.start_num = start_num
        self.stop_num = stop_num


    def take_input(self, point: int = None):
        if point == 1:
            point_text = self.start_text
            prompt = f"From Where Would You Like To {point_text}?\n"
        else:
            point_text = self.end_text
            prompt = f"Where Would You Like To {point_text}?\n"

        is_prompting = True
        while is_prompting:
            answer = input(prompt)
            if answer[0].lower() in self.stop_text_items:
                return False
            if answer == "":
                return 0
            elif answer.isnumeric():
                answer = int(answer)
                if answer < 0:
                    return 0
                elif 0 <= answer < self.total_num_items:
                    return answer
                elif answer > self.total_num_items:
                    prompt = f"The Number Must Be Between {point} and {self.total_num_items}"
            else:
                prompt = f"You Chose {answer}, That Is Not A Valid Entry\n"
                continue


    def take_inputs(self, start_text: str = None, end_text: str = None):
        if isinstance(start_text, str):
            self.start_text = start_text

        if self.start_num is None:
            point = 1
            start_num = self.take_input(point)
            if start_num is False:
                return False, False
        else:
            start_num = self.start_num


        if isinstance(end_text, str):
            self.end_text = end_text
        if self.stop_num is None:
            point = start_num+1
            stop_num = self.take_input(point)
            if stop_num is False:
                return start_num, False
        else:
            stop_num = self.stop_num

        return start_num, stop_num



if __name__ == "__main__":
    start, stop = TakeInput(500, None, None).take_inputs()
    print("Start Num: ", start)
    print("Stop Num: ", stop)

