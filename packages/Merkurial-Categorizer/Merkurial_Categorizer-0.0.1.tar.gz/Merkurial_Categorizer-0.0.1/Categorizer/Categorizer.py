import collections
import os
import copy
import shutil
import json

try:
    from FileUtils.paths import Dir
except ImportError:
    message = "Dir Must Be Installed To Run Categorizer\nYou May Run The Following Command To Install It:\n"
    message += "'pip install Merkurial-FileUtils>=0.0.0'\n\nAll Other Dependencies Are Pre-Packaged With Python"
    raise ImportError(message)


class Categorizer:
    def __init__(self, root_dir: str | Dir, latest_level, categories: dict | collections.OrderedDict | None = None,
                 move=False, debug_main: bool = None, debug: bool = None):
        """
        :param root_dir: The Full Directory Path Containing All The Folders You Want To Categorize
        :param latest_level: this is most likely just going to be an empty dictionary if you haven't categorized yet.
        :param categories: This is the categories Template Discussed later on.
        :param move: set to True If you want to actually move the directories
        :param debug_main: Default None, it is used for printing to give an idea of what might be going wrong in categorizeation
        :param debug: sames as debug_main but more detailed... lets say this means verbose
        """

        self.POINTER = root_dir if isinstance(root_dir, Dir) else Dir(root_dir)
        if categories is None:
            self.categories = {}
        elif isinstance(categories, collections.OrderedDict) or isinstance(categories, dict):
            self.categories = categories
        else:
            raise ValueError("Arg 'categories' must be of types 'dict' or 'collections.OrderedDict' or None")
        self.latest_level = {} if latest_level is None else latest_level
        self.debug = debug
        self.isDone = False
        self.vt = None
        self.verify = None
        self.current_category = None
        self.debug_main = debug_main

        self.image_group_path = None
        self.image_group_dirname = None
        self.move = move
        self.list_of_categories = []


    def verify_list_or_dict(self, vt, verify):
        title_name = self.image_group_dirname.title()

        if vt == dict or vt == collections.OrderedDict:
            if self.debug:
                print(f"Dict Verify {self.current_category}")
            for key in verify.keys():
                word_list = verify[key]
                for word in word_list:

                    if key == "main":
                        if word.title() in title_name:
                            if self.debug:
                                print(
                                    f"Main Word {word} Was In {self.image_group_dirname} IN Category "
                                    f"{self.current_category} ON KEYWORD IN {key}")
                            return True
                    elif key == "word":
                        for current_word in title_name.split(" "):
                            if word.title().strip() == current_word.strip():
                                if self.debug:
                                    print(
                                        f"Word {word} Matched {current_word} IN Category "
                                        f"{self.current_category} ON KEYWORD IN {key}")
                                return True
                    elif key == "phonics":
                        for sound in title_name.split(" "):
                            if word in sound:
                                if self.debug:
                                    print(
                                        f"Phonetic Sound {sound} Matched {word} IN Category "
                                        f"{self.current_category} ON KEYWORD IN {key}")
                                return True

        elif vt == list or vt == tuple:
            if self.debug:
                print("List Check")
            for word in verify:
                if self.debug:
                    print(f"Checking List For Word: '{word}' in {self.image_group_dirname} IN {self.current_category}")
                if word.title() in title_name:
                    if self.debug:
                        print(f"Word {word} Matched {self.image_group_path} IN Category {self.current_category}")
                    return True
        return False


    def Categorize(self, cleaned_group_name: str, categories: dict, latest_level: dict | collections.OrderedDict):
        if latest_level is None:
            raise ValueError("The Keyword Lists Must Be Supplied As The Latest Level")
        if categories is None:
            categories = {}

        cat_num = len(categories.keys()) + 1

        for category in iter(latest_level):
            if self.debug_main:
                self.debug_main = category
                print()
                print("Debugging")
                print("===================================================")
                print("Category: ", category)
                print("===================================================")
                print()

            if category == "__DIRECTORY__":
                if self.debug_main:
                    print(
                        "======================== "
                        "Congratulations You've Reached The Directory"
                        " ====================== =")

                latest_level = latest_level[category]
                return categories, latest_level, True


            cat = latest_level[category]
            sub = cat.get("sub")
            verify = cat.get('verify')
            callback = cat.get('callback')
            exceptions = cat.get("except")
            if self.debug_main:
                print("SUB: ", sub)
                print("VERIFY: ", verify)
                print("Callback: ", callback)

            vt = type(verify)
            vs = type(sub)

            returning = False

            if sub == "__EMPTY__":
                if self.debug_main:
                    print("__EMPTY__\nEnd Of Categorization For This Category")
                if callback:
                    returning = True
                    if self.debug_main:
                        print("There Is A Callback Returning Is Set To True")
                        print(f"RETURNING IS {returning}")

                elif verify:
                    returning = True

            elif sub == "__STOP__":
                if self.debug_main:
                    print("Stopping")
                categories[cat_num] = category
                return categories, latest_level, True

            if exceptions:
                if self.debug_main:
                    print("Running Through Exceptions")
                for exception in exceptions:
                    for word in cleaned_group_name.split(" "):
                        if exception.lower() == word.lower():
                            if self.debug_main:
                                print(
                                    f"Exception Skipped Category '{category}' As It Resolved As True ON: '{exception}' in {cleaned_group_name}")
                            continue
            if callback:
                if self.debug_main:
                    print(f"Going To Callback For Category {category}")

                callback_ans = callback(cleaned_group_name, self.debug_main)
                if callback_ans is not False and callback_ans is not None:
                    if self.debug_main:
                        print("Callback Answer In Categorize: ", callback_ans)
                        print(f"RETURNING IS {returning}")
                    categories[cat_num] = category

                    return categories, sub, returning
                else:
                    if self.debug_main:
                        print(f"{category} Callback Found No Matching Criteria")

            if verify is None:
                if self.debug_main:
                    print(f"Can't Verify {category}")
                if vs == dict or vs == list or vs == collections.OrderedDict:
                    if self.debug_main:
                        print("Sending Back Sub")
                    categories[cat_num] = category
                    return categories, sub, returning
                else:
                    # Means That Both Verify And Sub Are No Good For Sorting
                    if self.debug_main:
                        print("Sending Back The Next Category")
                    return categories, categories[category], False

            elif vt == dict or vt == collections.OrderedDict or vt == list or vt == tuple:
                if self.debug_main:
                    print(f"Verifying {category}")
                ans = self.verify_list_or_dict(vt, verify)
                if ans:
                    categories[cat_num] = category
                    return categories, sub, returning
                else:
                    continue

            else:
                if self.debug_main:
                    print(f"Tried To Verify Category {category} But Failed")
                if sub:
                    # print("Sending Sub Back")
                    return categories, sub, False
                else:
                    # print("Sending Category Back")
                    return categories, latest_level[category], False

        raise ValueError("The Categories Supplied Were Empty")


    @staticmethod
    def update_json(new_dir_path: str, categories: dict):
        json_path = os.path.join(new_dir_path, "meta.json")
        with open(json_path, "r+") as json_file:
            data = json.load(json_file)
        data["Directory"] = new_dir_path
        data["Categories"] = categories

        with open(json_path, "w+") as json_file:
            json.dump(data, json_file, indent=4)


    def move_directory(self):
        category_dir = Dir(os.path.join(self.POINTER.path))
        for cat in self.categories.values():
            category_dir.dig(cat)

        # This Variable Is Needed As shutil.move Requires The Parent Directory Not The Full Path
        ending_path_for_not_moving = os.path.join(category_dir.path, self.image_group_dirname)

        if self.image_group_path.strip() != ending_path_for_not_moving:
            try:
                stringed_categories = {}
                print(f"From:\n{self.image_group_path}\nTo:\n{ending_path_for_not_moving}")
                for cat in self.categories.keys():
                    stringed_categories[str(cat)] = self.categories[cat]
                shutil.move(self.image_group_path, category_dir.path)
                self.update_json(ending_path_for_not_moving, stringed_categories)
            except shutil.Error as err:
                if "already exists" in str(err):
                    pass
                else:
                    print("Error Moving Files")
                    print("Err: ", err)
        else:
            print(f"Tried To Replace Directory With Itself: \n{ending_path_for_not_moving}")
            print("Starting And Ending Paths Are The Same")


    def categorize_one(self, latest_level: collections.OrderedDict, categories):
        self.isDone = False
        while not self.isDone:
            categories, latest_level, self.isDone = \
                self.Categorize(self.image_group_dirname, categories, latest_level)
        return categories, latest_level



    def categorize(self):
        for self.image_group_path, directories, group_files in os.walk(self.POINTER.path):
            self.image_group_dirname = os.path.split(self.image_group_path)[-1]
            if "meta.json" in group_files:
                self.categories = {}
                latest_level = copy.deepcopy(self.latest_level)
                categories, latest_level = self.categorize_one(latest_level, self.categories)
                self.categories = categories
                self.list_of_categories.append(categories)
                if self.move:
                    self.move_directory()

        return self.list_of_categories,




