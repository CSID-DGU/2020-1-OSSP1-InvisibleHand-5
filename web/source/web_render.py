
def bio(character, ratio_list):
    text = f"""
        <div class="charContainer">
            <div class="bio">
                <span class="bio_name">{character}</span>
            </div>
            <div class="content">
                <div class="data">
                    <ul>
                        <li>
                            {ratio_list[0]}%
                            <span class="happy">기쁨</span>
                        </li>
                        <li>
                            {ratio_list[1]}%
                            <span class="sad">슬픔</span>
                        </li>
                        <li>
                            {ratio_list[2]}%
                            <span class="anger">분노</span>
                        </li>
                    </ul>
                    <ul>
                        <li>
                            {ratio_list[3]}%
                            <span class="fear">공포</span>
                        </li>
                        <li>
                            {ratio_list[4]}%
                            <span class="disgust">혐오</span>
                        </li>
                        <li>
                            {ratio_list[5]}%
                            <span>놀람</span>
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