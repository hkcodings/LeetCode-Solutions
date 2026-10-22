class Solution {
    public boolean containsDuplicate(int[] nums) {
    HashSet<Integer> Set1 = new HashSet<>();

    for(int i = 0; i<nums.length; i++) {
        if(Set1.contains(nums[i])){
            return true;
        } 

        Set1.add(nums[i]);
    }
    return false;
    }
}