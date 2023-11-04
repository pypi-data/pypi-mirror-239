from fuzzywuzzy import fuzz
from sinlingua.grammar_rule.grammar_rules import GrammarRules
from sinlingua.src.grammar_rule_resources import past_verbs


class PastSecondPersonPlural(GrammarRules):
    def common_function(self, sentence):
        global conjugated_sentence
        grammar_obj = GrammarRules()
        conjugated_verb = ''

        # call the function find verb of sentence
        returned_string_verb = grammar_obj.find_similar_words(past_verbs, sentence)

        verb_checked = returned_string_verb[0]

        actual_word = returned_string_verb[1]

        ratio = returned_string_verb[2]

        if returned_string_verb[0]:
            # Extract the verb stem
            verb_stem = verb_checked[:-1]

            # Split the sentence and Remove the last word (verb) from the sentence
            words = sentence.split()
            words.remove(actual_word)

            # Check if the sentence starts with "ඔවුන්" or "ඔවුහු"
            if sentence.split()[0] in ["ඔවුන්", "ඔවුහු"] or (len(sentence.split()) > 1 and sentence.split()[1] in ["ඔවුන්", "ඔවුහු"]):
                if len(words) > 1 and words[1] in ["ඔවුන්", "ඔවුන්"]:
                    words.pop(0)
                conjugated_verb = verb_stem + "ෝය"

                # Append the conjugated verb to the sentence
            words.append(conjugated_verb)

            # Reconstruct the sentence
            conjugated_sentence = " ".join(words)

        if conjugated_verb == '':
            return "Try Again..Incomplete sentence. No enough data to process", ratio

        else:
            return conjugated_sentence, ratio
