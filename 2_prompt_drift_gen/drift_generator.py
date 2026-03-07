import json
import random
import re


# =====================================================
# TRANSFORMATIONS
# =====================================================

class DriftTransforms:

    def __init__(self):

        self.KEYBOARD_ADJ = {
            'a': ['s', 'q', 'z'], 'b': ['v', 'n', 'g'], 'c': ['x', 'v', 'd'],
            'd': ['s', 'f', 'e', 'c'], 'e': ['w', 'r', 'd'], 'f': ['d', 'g', 'r'],
            'g': ['f', 'h', 't'], 'h': ['g', 'j', 'y'], 'i': ['u', 'o', 'k'],
            'j': ['h', 'k', 'u'], 'k': ['j', 'l', 'i'], 'l': ['k', 'o', 'p'],
            'm': ['n', 'k'], 'n': ['b', 'm', 'h'], 'o': ['i', 'p', 'l'],
            'p': ['o', 'l'], 'q': ['w', 'a'], 'r': ['e', 't', 'f'],
            's': ['a', 'd', 'w', 'z'], 't': ['r', 'y', 'g'], 'u': ['y', 'i', 'j'],
            'v': ['c', 'b', 'f'], 'w': ['q', 'e', 's'], 'x': ['z', 'c', 's'],
            'y': ['t', 'u', 'h'], 'z': ['a', 'x', 's']
        }

        self.COMMON_TYPOS = {
            'the': ['teh', 'hte', 'th'], 'and': ['adn', 'nd', 'an'], 
            'that': ['taht', 'tht', 'tat'], 'this': ['tihs', 'ths', 'dis'],
            'with': ['wiht', 'wth', 'wit'], 'have': ['hvae', 'hve', 'hav'],
            'from': ['form', 'frm', 'fro'], 'they': ['tehy', 'thy', 'tey'],
            'been': ['bene', 'ben', 'bee'], 'when': ['wehn', 'wen', 'whe'],
            'than': ['tahn', 'thn', 'tha'], 'should': ['shuold', 'shld', 'shoud'],
            'would': ['wuold', 'wld', 'woud'], 'could': ['cuold', 'cld', 'coud'],
            'because': ['becuase', 'bcoz', 'bcz', 'bc'], 'through': ['througt', 'thru', 'thro'],
            'which': ['whcih', 'wich', 'whch'], 'about': ['abuot', 'abt', 'bout'],
            'whether': ['whetehr', 'whetr', 'wether'], 'between': ['beween', 'btwn', 'btween'],
            'explain': ['explian', 'xplain', 'explan'], 'system': ['systme', 'sys', 'systm'],
            'important': ['importnat', 'imp', 'impt'], 'consider': ['consdier', 'consdr', 'considr'],
            'question': ['questoin', 'ques', 'qstion'], 'different': ['diffrent', 'diff', 'diffrnt'],
            'government': ['goverment', 'govt', 'gvt'], 'decision': ['decisoin', 'dcsn', 'decison'],
            'information': ['informaton', 'info', 'infrmtn'], 'organization': ['organisaton', 'org', 'orgzn']
        }

        self.SLANG_MAP = {
            'you': 'u', 'your': 'ur', 'are': 'r', 'to': '2', 'too': '2',
            'for': '4', 'be': 'b', 'see': 'c', 'please': 'pls', 'thanks': 'thx',
            'because': 'bc', 'without': 'w/o', 'with': 'w/', 'and': 'n', '&': 'n',
            'people': 'ppl', 'between': 'btwn', 'about': 'abt', 'information': 'info',
            'organization': 'org', 'management': 'mgmt', 'government': 'govt',
            'technology': 'tech', 'approximately': 'approx', 'example': 'eg', 'versus': 'vs',
            'however': 'tho', 'therefore': 'so', 'important': 'imp', 'something': 'smth',
            'explain': 'xplain', 'regarding': 're', 'definitely': 'def', 'someone': 'sum1',
            'probably': 'prob', 'actually': 'actly', 'basically': 'bsclly', 'through': 'thru',
            'before': 'b4', 'after': 'aftr', 'should': 'shld', 'would': 'wld', 'could': 'cld',
            'nothing': 'nothin', 'something': 'smthn', 'everything': 'evrything', 'anyone': 'any1',
            'question': 'q', 'answer': 'ans', 'think': 'thnk', 'need': 'nd', 'want': 'wnt',
            'right': 'rite', 'know': 'kno', 'going': 'goin', 'doing': 'doin', 'trying': 'tryin'
        }

        self.DROP_WORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'of', 'in', 'to', 'at', 
              'by', 'on', 'with', 'from', 'as', 'into', 'during'}

    # --------------------------------------------------

    def level1_typos(self, text, typo_rate, seed):
        random.seed(seed)
        words = text.split()
        result = []
        for word in words:
            if random.random() < typo_rate and len(word) > 2:
                lower = word.lower()
                # --- Common typo (higher priority) ---
                if lower in self.COMMON_TYPOS and random.random() < 0.5:
                    typo = random.choice(self.COMMON_TYPOS[lower])
                    # preserve capitalization
                    if word[0].isupper():
                        typo = typo.capitalize()
                    result.append(typo)
                # --- Keyboard adjacency typo ---
                else:
                    chars = list(word)
                    if len(chars) > 2:
                        idx = random.randint(1, len(chars) - 2)
                        c = chars[idx].lower()

                        if c in self.KEYBOARD_ADJ:
                            chars[idx] = random.choice(self.KEYBOARD_ADJ[c])
                    result.append("".join(chars))
            else:
                result.append(word)
        return " ".join(result)

    # --------------------------------------------------

    def level2_formatting(self, text, punct_rate, seed):
        random.seed(seed)
        text = text.lower()
        for p in [".", ",", ";", ":", "?", "!"]:
            if random.random() < punct_rate:
                text = text.replace(p, "")
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------------------

    def level3_slang(self, text, slang_rate, seed):
        random.seed(seed)
        words = text.split()
        out = []
        for w in words:
            clean = re.sub(r"[^a-zA-Z]", "", w).lower()
            # --- direct slang map replacement ---
            if clean in self.SLANG_MAP and random.random() < slang_rate:
                out.append(self.SLANG_MAP[clean])
            # --- fallback slang-style distortion ---
            elif random.random() < slang_rate * 0.4 and len(clean) > 4:
                r = random.random()
                # drop vowels (information → informtion)
                if r < 0.33:
                    distorted = re.sub(r"[aeiou]", "", clean)
                # truncate word (because → beca)
                elif r < 0.66:
                    distorted = clean[:max(3, int(len(clean)*0.7))]
                # remove 'g' in ing (going → goin)
                else:
                    distorted = re.sub(r"ing$", "in", clean)
                out.append(distorted)
            else:
                out.append(w)
        return " ".join(out)

    # --------------------------------------------------

    def level4_structure(self, text, merge_prob, drop_prob, seed):
        random.seed(seed)
        words = text.split()
        out = []
        i = 0
        while i < len(words):
            r = random.random()
            if r < merge_prob and i + 1 < len(words):
                out.append(words[i] + words[i+1])
                i += 2
                continue
            if r < drop_prob and words[i].lower() in self.DROP_WORDS:
                i += 1
                continue
            out.append(words[i])
            i += 1

        return " ".join(out)

    # --------------------------------------------------

    def level5_informal(self, text, cut_range, caps_prob, seed):
        random.seed(seed)
        openers = [
        "hey ", "ok so ", "basically ", "listen ", "yo ", "btw ",
        "just saying ", "quick note ", "fyi ", "so like ",
        "tbh ", "real quick ", "lowkey ", "honestly ",
        "alright ", "so yeah ", "uhh ", "hmm "
        ]

        closers = [
        "??", "!!", " pls", " asap", " lol", " haha",
        " btw", " tho", " fr", " tbh", " right?",
        " yeah?", " ok?", " got it?", " pls?", 
        " thanks", " ty", " appreciate it"
        ]

        words = text.split()
        cut_rate = random.uniform(cut_range[0], cut_range[1])
        keep = max(int(len(words) * cut_rate), 5)
        words = words[:keep]
        text = random.choice(openers) + " ".join(words) + random.choice(closers)
        words = text.split()

        for i in range(len(words)):

            if random.random() < caps_prob:
                words[i] = words[i].upper()

        return " ".join(words)


# =====================================================
# DRIFT ENGINE
# =====================================================

class PromptDrifter:
    LEVEL_ORDER = ["L1", "L2", "L3", "L4", "L5"]

    def __init__(self, category_configs):
        self.transforms = DriftTransforms()
        self.configs = category_configs

    # --------------------------------------------------

    def apply_level(self, text, level, params, seed):
        if level == "L1":
            return self.transforms.level1_typos(
                text,
                params["typo_rate"],
                seed
            )

        if level == "L2":
            return self.transforms.level2_formatting(
                text,
                params["punct_rate"],
                seed
            )

        if level == "L3":
            return self.transforms.level3_slang(
                text,
                params["slang_rate"],
                seed
            )

        if level == "L4":
            return self.transforms.level4_structure(
                text,
                params["merge_prob"],
                params["drop_prob"],
                seed
            )

        if level == "L5":
            return self.transforms.level5_informal(
                text,
                params["cut_range"],
                params["caps_prob"],
                seed
            )

        return text

    # --------------------------------------------------

    def generate_variants(self, prompt_id, prompt_text, category):
        config = self.configs[category]
        variants = []

        for level in self.LEVEL_ORDER:

            for variant in range(3):

                seed = hash((prompt_id, level, variant))
                text = prompt_text

                for lvl in self.LEVEL_ORDER:

                    if lvl not in config:
                        continue

                    text = self.apply_level(
                        text,
                        lvl,
                        config[lvl],
                        seed
                    )

                    if lvl == level:
                        break

                variants.append({
                    "id": f"{prompt_id}_{level}_V{variant+1}",
                    "base_id": prompt_id,
                    "category": category,
                    "drift_level": int(level[1]),
                    "variant": variant + 1,
                    "prompt": text
                })

        return variants


# =====================================================
# MAIN PIPELINE
# =====================================================

def main():

    random.seed(42)

    with open("../1_dataset_prep/ideal_prompts.json") as f:
        data = json.load(f)

    # --------------------------------------------------
    # CATEGORY CONFIGS
    # --------------------------------------------------

    reasoning_config = {

        "L1": {"typo_rate": 0.10},

        "L2": {"punct_rate": 0.72},

        "L3": {"slang_rate": 0.5},

        "L4": {
            "merge_prob": 0.25,
            "drop_prob": 0.35
        },

        "L5": {
            "cut_range": (0.60, 0.75),
            "caps_prob": 0.08
        }
    }

    logical_config = {

        "L1": {"typo_rate": 0.08},

        "L2": {"punct_rate": 0.65},

        "L3": {"slang_rate": 0.52},

        "L4": {
            "merge_prob": 0.45,
            "drop_prob": 0.35
        },

        "L5": {
            "cut_range": (0.65, 0.75),
            "caps_prob": 0.06
        }
    }

    classification_config = {

        "L1": {"typo_rate": 0.08},

        "L2": {"punct_rate": 0.65},

        "L3": {"slang_rate": 0.45},

        "L4": {
            "merge_prob": 0.25,
            "drop_prob": 0.35
        },

        "L5": {
            "cut_range": (0.60, 0.75),
            "caps_prob": 0.08
        }
    }

    qna_config = {

        "L1": {"typo_rate": 0.12},

        "L2": {"punct_rate": 0.85},

        "L3": {"slang_rate": 0.6},

        "L4": {
            "merge_prob": 0.40,
            "drop_prob": 0.40
        },

        "L5": {
            "cut_range": (0.60, 0.70),
            "caps_prob": 0.05
        }
    }

    category_configs = {

        "reasoning": reasoning_config,
        "logical": logical_config,
        "classification": classification_config,
        "qna": qna_config
    }

    # --------------------------------------------------

    drifter = PromptDrifter(category_configs)

    all_prompts = []

    for p in data["prompts"]:

        # L0 (clean baseline)
        all_prompts.append({
            "id": f"{p['id']}_L0",
            "base_id": p["id"],
            "category": p["category"],
            "drift_level": 0,
            "variant": 0,
            "prompt": p["prompt"]
        })

        # L1–L5 variants
        variants = drifter.generate_variants(
            p["id"],
            p["prompt"],
            p["category"]
        )

        all_prompts.extend(variants)

        output = {
        "metadata": {
            "project": data["metadata"]["project"],
            "description": "Drift-augmented prompt dataset with 5 levels x 3 variants per base prompt (STRONGER degradation)",
            "total_base_prompts": 40,
            "drift_levels": 5,
            "variants_per_level": 3,
            "total_drifted_prompts": 40 * 5 * 3,
            "total_prompts_including_base": 40 + (40 * 5 * 3),
            "target_similarities": {
                "L1": "96-99% (mild typos)",
                "L2": "93-96% (+ no caps/punct)",
                "L3": "88-93% (+ slang)",
                "L4": "82-88% (+ structural degradation)",
                "L5": "75-82% (+ heavy informality, incomplete)"
            },
            "drift_level_descriptions": {
                "L0": "Clean baseline - original prompt unchanged",
                "L1": "Character-level typos only (~12-24% word error rate)",
                "L2": "L1 + informal formatting (no caps, punctuation removed)",
                "L3": "L2 + slang, abbreviations, casual language",
                "L4": "L3 + structural degradation (word merges, drops, grammar breaks)",
                "L5": "L4 + heavy informality, content dropped, fragments"
            }
        },
        "prompts": all_prompts
    }

    with open("drifted_prompts.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Drift generation complete")


if __name__ == "__main__":
    main()