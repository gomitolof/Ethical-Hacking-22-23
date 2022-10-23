#define NULL 0 

class Solution {
public:
    string vowel(string word) {
        return word + "ma";
    }
    
    string cons(string word) {
        string new_word = word.substr(1,word.length());
        return new_word + word[0] + "ma";
    }
    
    string push_a(string word, int i) {
        string new_word = word;
        for(int j=0; j<i; j++){
            new_word = new_word + "a";
        }
        return new_word;
    }
    
    string toGoatLatin(string sentence) {
        int n = sentence.length();
 
        // declaring character array
        char new_sentence[n + 1];
        string ns = "";
        // copying the contents of the
        // string to char array
        strcpy(new_sentence, sentence.c_str());
        char* ptr = strtok(new_sentence, " ");
        int i=0;
        while(ptr != NULL)
        {
            i++;
            string new_word = "";
            if(tolower(*ptr) == 'a'|| tolower(*ptr) == 'e' || tolower(*ptr) == 'i' || tolower(*ptr) =='o' || tolower(*ptr) =='u'){
                new_word = vowel(ptr);
            }
            else{
                new_word = cons(ptr);
            }
            new_word = push_a(new_word, i) + " ";
            ns = ns + new_word;
            ptr = strtok (NULL, " ");
        }
        return ns.substr(0,ns.length()-1);
    }
};