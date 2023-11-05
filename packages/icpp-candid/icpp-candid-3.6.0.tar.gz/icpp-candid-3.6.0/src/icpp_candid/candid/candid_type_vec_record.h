// The class for the Candid Type: text

#pragma once

#include <cstring>

#include "candid_args.h"
#include "candid_type_record.h"
#include "vec_bytes.h"

class CandidTypeVecRecord : public CandidTypeBase<CandidTypeVecRecord> {
public:
  // Constructors
  CandidTypeVecRecord();
  CandidTypeVecRecord(const CandidTypeRecord v);

  CandidTypeVecRecord(CandidTypeRecord *p_v);

  // Destructor
  ~CandidTypeVecRecord();

  bool decode_M(CandidDeserialize &de, VecBytes B, __uint128_t &offset,
                std::string &parse_error);

  CandidTypeRecord get_v() { return m_v; }
  CandidTypeRecord *get_pv() { return m_pv; }
  std::shared_ptr<CandidTypeRecord> get_pr() { return m_pr; }

  bool decode_T(VecBytes B, __uint128_t &offset, std::string &parse_error);

protected:
  void set_pv(CandidTypeRecord *v) { m_pv = v; }
  void set_v(const CandidTypeRecord &v) { m_v = v; }
  void set_content_type();
  void encode_M();

  CandidTypeRecord m_v;
  CandidTypeRecord *m_pv{nullptr};

  void create_dummy_record();
  // a shared pointer to the dummy record
  std::shared_ptr<CandidTypeRecord> m_pr{nullptr};

  void initialize();
  void set_datatype();
  void encode_T();
  void encode_I();
};