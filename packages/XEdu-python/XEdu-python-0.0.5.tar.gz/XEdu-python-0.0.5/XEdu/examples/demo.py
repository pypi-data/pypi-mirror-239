#coding=utf-8

from XEdu.hub import Workflow as wf
import cv2
import numpy as np 


def pose_infer_demo():
    # a = time.time()
    img = 'eason.png' # 指定进行推理的图片路径
    pose = wf(task='body')# ,checkpoint="rtmpose-m-80e511.onnx") # 实例化mmpose模型

    result,img = pose.inference(data=img,img_type='pil') # 在CPU上进行推理
    print(result)
    pose.show(img)
    # pose.save(img,"pimg_ou.png")
    
    result = pose.format_output(lang="zh")
    # print(result)

def video_infer_demo():
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("gyt.mp4")
    
    pose = wf(task='pose_body')
    det = wf(task='det_body')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        bboxs = det.inference(data=frame,thr=0.3) # 在CPU上进行推理
        img = frame
        for i in bboxs:
            keypoints,img =pose.inference(data=img,img_type='cv2',bbox=i) # 在CPU上进行推理
        cv2.imshow('video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    cap.release()
    cv2.destroyAllWindows()

def det_infer_demo():
    # a = time.time()
    from XEdu.hub import Workflow as wf
    img = 'pose4.jpg' # 指定进行推理的图片路径

    det = wf(task='det_body')#,checkpoint='rtmdet-acc0de.onnx')# ,checkpoint="rtmpose-m-80e511.onnx") # 实例化mmpose模型

    bboxs,im_ou = det.inference(data=img,img_type='cv2',thr=0.3,show=True) # 在CPU上进行推理
    # print(bboxs)
    # det.save(im_ou,"im_ou_d.jpg")

    det.format_output(lang="zh")
    # print(result)

def hand_video_demo():
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("pose.mp4")

    pose = wf(task='pose_hand21')# ,checkpoint="rtmpose-m-80e511.onnx") # 实例化pose模型

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        keypoints,img =pose.inference(data=frame,img_type='cv2') # 在CPU上进行推理
        cv2.imshow('video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    cap.release()
    cv2.destroyAllWindows()

def coco_det_demo():
    img = 'pose1.jpg' # 指定进行推理的图片路径
    det = wf(task='det_coco') # 实例化mmpose模型

    result,img = det.inference(data=img,img_type='cv2') # 在CPU上进行推理
    det.show(img)
    # det.save(img,"pimg_ou.png")
    
    re = det.format_output(lang="zh")

def face_det_demo():
    img = 'pose3.jpg' # 指定进行推理的图片路径
    # img = 'face2.jpeg' # 指定进行推理的图片路径

    det = wf(task='det_face' )
    face = wf(task="pose_face")

    result,img = det.inference(data=img,img_type='cv2') # 在CPU上进行推理
    det.show(img)
    for i in result:
        ky,img = face.inference(data=img, img_type="cv2",bbox=i)#,erase=False)
        face.show(img)
    
    # re = face.format_output(lang="zh")

def ocr_demo():
    img = 'ocr.jpg' # 指定进行推理的图片路径
    ocr = wf(task='ocr' )#,checkpoint="rtmdet-coco.onnx") # 实例化mmpose模型

    result,img = ocr.inference(data=img,img_type='pil',show=True) # 在CPU上进行推理
    # print(result)
    # ocr.show(img)
    ocr.save(img,"pimg_ou.png")
    
    re = ocr.format_output(lang="zh")

def mmedu_demo():

    mm = wf(task='mmedu',checkpoint="det_fire.onnx")
    result, img = mm.inference(data='fire.jpg',img_type='pil',thr=0.6)
    mm.show(img)
    print(result)
    re = mm.format_output(lang="zh")

def basenn_demo():

    nn = wf(task='basenn',checkpoint="checkpoints/basenn.onnx") # iris act 
    result,img = nn.inference(data='6.jpg',img_type='cv2')
    re = nn.format_output(lang="zh")
    nn.show(img)

def hand_det_demo():
    img = 'hand4.jpeg' # 指定进行推理的图片路径
    det = wf(task='det_hand') # 实例化mmpose模型
    hand = wf(task='pose_hand')

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result,img = det.inference(data=frame,img_type='cv2',thr=0.3) # 在CPU上进行推理
        for i in result:
            ky, img = hand.inference(data=img, img_type='cv2',bbox=i)
        cv2.imshow('video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    cap.release()
    cv2.destroyAllWindows()
    # det.save(img,"pimg_ou.png")
    # re = det.format_output(lang="zh")

def custom_demo():
    def pre(path):
        img = cv2.imread(path) 
        img = img.astype(np.float32)
        img = np.expand_dims(img,0) # 增加batch维
        img = np.transpose(img, (0,3,1,2)) # [batch,channel,width,height]
        return img
    
    def post(res,data):
        
        idx = np.argmax(res[0])
        # print(xxx)
        return idx, res[0][0][idx]

    img_path = "ele.jpg"
    mm = wf(task='custom',checkpoint="mobileone-s3-46652f.onnx") # iris act 
    result = mm.inference(data=img_path,preprocess=pre,postprocess=post)
    print(result)

def cls_demo():
    cls = wf(task='cls_imagenet')#checkpoint="mobileone-s3-46652f.onnx") # iris act 
    img = cv2.imread('ele.jpg')
    result,img = cls.inference(data="ele.jpg",img_type="pil")
    cls.show(img)
    # print(result)
    re = cls.format_output(lang="zh")

def baseml_demo():
    ml = wf(task='baseml',checkpoint="mymodel.pkl") # iris act 
    result = ml.inference(data=[[1,0.5,-1,0]])
    re = ml.format_output(lang="zh")

def sup_demo():
    from transformers import AutoTokenizer
    from onnxruntime import InferenceSession
    import numpy as np

    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    session = InferenceSession("all-MiniLM-L6-v2/model.onnx")
    # ONNX Runtime expects NumPy arrays as input
    inputs1 = tokenizer("hi", return_tensors="np")
    inputs2 = tokenizer("hello hi", return_tensors='np')
    print("inputs",inputs1,inputs2)
    vec1 = np.squeeze(session.run(output_names=["last_hidden_state"], input_feed=dict(inputs1))[0].reshape(1,-1))
    vec2 = np.squeeze(session.run(output_names=["last_hidden_state"], input_feed=dict(inputs2))[0].reshape(1,-1))
    print("outputs",vec1[:10],vec2[:10])

    cos_sim = vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    print(cos_sim)

def style():
    # for i in range(5):
    #     style = wf(task='gen_style' ,style=i) # iris act 
    #     result = style.inference(data="ele.jpg" ,img_type='cv2')
    #     style.show(result)
    #     result,img = style.inference(data="ele.jpg" ,img_type='cv2')
    #     style.show(result)
    #     result,img = style.inference(data="ele.jpg" ,img_type='pil')
    #     style.show(result)
    #     result = style.inference(data="ele.jpg" ,img_type='pil')
    #     style.show(result)
        # style.format_output(lang="zh")
        # cv2.imshow("img",img)
        # cv2.imshow("result",result)
        # cv2.waitKey(0)
        # style.show(img)
    
    style = wf(task='gen_style',style=0) 
    result,img = style.inference(data="ele.jpg",img_type='pil')
    
    # style.show(result)
    # 打开摄像头，实时风格迁移
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result,img = style.inference(data=frame,img_type='cv2')
        cv2.imshow('video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def sim():
    from onnxsim import simplify
    import onnx
    model = onnx.load("udnie-9.onnx")
    model,_ = simplify(model)
    onnx.save(model, "gen_style_udnie.onnx")

if __name__ == "__main__":
    # pose_infer_demo()
    # det_infer_demo()
    # video_infer_demo()
    # hand_video_demo()
    # coco_det_demo()
    # hand_det_demo()
    # face_det_demo()
    # ocr_demo()
    # mmedu_demo()
    # custom_demo()
    # basenn_demo()
    # cls_demo()
    # baseml_demo()
    # sup_demo()
    # whisper()
    style()

