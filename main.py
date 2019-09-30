

from search_dictionary import search
from tempInfrastructure.CCS import interact_model, get_candidates, choose_sentence
'''
while iter < MAX_ITER:
    if best sentence contains goal_word:
        return final_output
    if best_sentence is > n similar to goal_word:
        return final_output
    interact_model(input=best_sentence)
    iter =+ 1

return final_output

'''


if __name__ == '__main__':
    output = 0
    while output == 0:
        in_words = input("Enter a starting words and goal word separated by space: ")
        # TODO make this more robust, don't leave the input form up to the user
        start_word, goal_word = in_words.split()
        output =  search(start_word)
    MAX_ITER = 5
    iter = 0
    while iter < MAX_ITER:
        print("generating text...")
        gpt2_output = interact_model(output)
        candidates = get_candidates(gpt2_output, goal_word)
        chosen_candidate = choose_sentence(candidates)
        print("chosen candidate:", chosen_candidate)

        output += chosen_candidate
        print ("iteration: "+ iter +" output: "+output)

        if goal_word in chosen_candidate:
            print("iteration: "+ iter +" output: "+output)
            break
        iter += 1
    print("Max iterations reached")
    print("final output: ",output)


    # generate_text(start_word, goal_word)
