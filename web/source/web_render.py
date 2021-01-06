
def bio(character, ratio_list, emo):
    text = f"""
        <div class="charContainer">
            <div class="bio">
                <span class="bio_name">{character} ({emo})</span>
            </div>
            <div class="content">
                <div class="data">
                    <ul>
                        <li>
                            <span class="happy">{ratio_list[0]}%</span>
                            <span class="happy">기쁨</span>
                        </li>
                        <li>
                            <span class="sad">{ratio_list[1]}%</span>
                            <span class="sad">슬픔</span>
                        </li>
                        <li>
                            <span class="anger">{ratio_list[2]}%</span>
                            <span class="anger">분노</span>
                        </li>
                    </ul>
                    <ul>
                        <li>
                            <span class="fear">{ratio_list[3]}%</span>
                            <span class="fear">공포</span>
                        </li>
                        <li>
                            <span class="disgust">{ratio_list[4]}%</span>
                            <span class="disgust">혐오</span>
                        </li>
                        <li>
                            <span class="surprise">{ratio_list[5]}%</span>
                            <span class="surprise">놀람</span>
                        </li>
                    </ul>
                </div>

                <div class="emo">
                    <div class="view_dataframe"></div> 결과 보기
                </div>
            </div>
        </div>
        """
    return text
