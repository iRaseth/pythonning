from chess_rating.infrastructure.transformer.transform import Transform

def test_transform_data_to_profile():
    fake_data ={"belmund": 213}
    object = Transform()

    result = object.transform_data_to_profile(fake_data)
    to_dict_result = result.to_dict()

    assert to_dict_result == {"nazwa": "belmund", "rating": 213}
